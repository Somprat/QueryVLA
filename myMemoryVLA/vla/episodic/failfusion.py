import torch
import torch.nn.functional as F
import torch.nn as nn


class CrossTransformerBlock(nn.Module):
    def __init__(self, feature_dim: int):
        super().__init__()
        self.q_proj = nn.Linear(feature_dim, feature_dim)
        self.k_proj = nn.Linear(feature_dim, feature_dim)
        self.v_proj = nn.Linear(feature_dim, feature_dim)
        self.attn_norm = nn.LayerNorm(feature_dim)

        # Feed‑Forward Network
        self.ffn = nn.Sequential(
            nn.Linear(feature_dim, feature_dim * 4),
            nn.GELU(),
            nn.Linear(feature_dim * 4, feature_dim)
        )
        self.ffn_norm = nn.LayerNorm(feature_dim)

    def forward(self,
                query: torch.Tensor, # (B, N, D)
                k: torch.Tensor, # (B, M, D)
                v: torch.Tensor, # (B, M, D)
                ) -> torch.Tensor:
        q = self.q_proj(query)
        k = self.k_proj(k)
        v = self.v_proj(v)
        attn_out = F.scaled_dot_product_attention(q, k, v, dropout_p=0.0, is_causal=False)

        # residual + LN
        x = self.attn_norm(query + attn_out)

        # FFN + LN
        ffn_out = self.ffn(x)
        return self.ffn_norm(x + ffn_out)


class FailAwareFusion(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.fail_attn = CrossTransformerBlock(dim)

        self.risk_head = nn.Sequential(
            nn.Linear(dim * 4, dim),
            nn.GELU(),
            nn.Linear(dim, 1),
        )

        self.correction = nn.Sequential(
            nn.Linear(dim * 2, dim),
            nn.GELU(),
            nn.Linear(dim, dim),
        )
        nn.init.zeros_(self.correction[-1].weight)
        nn.init.zeros_(self.correction[-1].bias)
        nn.init.constant_(self.risk_head[-1].bias, -4.0)

    def forward(self, current, fail_memory):
        if fail_memory is None:
            risk = current.new_zeros((*current.shape[:-1], 1))
            return current, risk

        fail_memory = fail_memory.to(device=current.device, dtype=current.dtype)
        if fail_memory.ndim == 2:
            fail_memory = fail_memory.unsqueeze(0)

        failure_context = self.fail_attn(
            current,
            fail_memory,
            fail_memory
        )

        comparison = torch.cat([
            current,
            failure_context,
            torch.abs(current - failure_context),
            current * failure_context
        ], dim=-1)

        risk = torch.sigmoid(self.risk_head(comparison))

        correction = self.correction(
            torch.cat([current, failure_context], dim=-1)
        )

        output = current + risk*correction

        return output, risk

"""Regression tests for evaluation retrieval strategies; no checkpoint required."""
import argparse
import ast
from pathlib import Path
import unittest
from unittest.mock import patch

import torch
from vla.memory_vla import BankEntry, CogMemBank
from vla.spatial.retrieval import MemoryRetriever


class CaptureContext(torch.nn.Module):
    def forward(self, query, key, value):
        self.context = value
        return query


class RetrievalModesTest(unittest.TestCase):
    def bank(self, mode):
        bank = CogMemBank.__new__(CogMemBank)
        torch.nn.Module.__init__(bank)
        bank.query_retrieval_mode = mode
        bank.query_retrieval_top_k = 4
        bank.query_retriever = MemoryRetriever()
        bank.use_timestep_pe = False
        bank.fusion_type = 'add'
        bank.update_fused = False
        bank.mem_length = 20
        bank.consolidate_type = 'fifo'
        bank.retrieval_blocks = torch.nn.ModuleList([CaptureContext()])
        vectors = [[-1., 0.], [-0.5, 1.], [0., 1.], [0.5, 1.], [1., 0.]]
        bank.bank = {0: [BankEntry(torch.tensor(i), torch.tensor([v]),
                                  torch.tensor(v), ('test',))
                         for i, v in enumerate(vectors)]}
        bank.eval()
        return bank

    def test_cosine_forward_selects_four_in_similarity_order(self):
        bank = self.bank('cosine')
        original = list(bank.bank[0])
        bank.process_batch(torch.tensor([[[1., 0.]]]), [0], [100],
                           instructions=['go back to the previous location'],
                           retrieval_query_embeddings=torch.tensor([[1., 0.]]))
        expected = torch.stack([original[i].feat for i in [4, 3, 2, 1]]).reshape(1, 4, 2)
        torch.testing.assert_close(bank.retrieval_blocks[0].context, expected)

    def test_cosine_falls_back_to_features_for_missing_embedding(self):
        bank = self.bank('cosine')
        hist = bank.bank[0]
        hist[0].image_embedding = None
        selected = bank._select_history(hist, torch.tensor([[[1., 0.]]]), '', 0,
                                        query_embedding=torch.ones(7))
        self.assertEqual([id(x) for x in selected], [id(hist[i]) for i in [4, 3, 2, 1]])

    def test_shuffled_forward_uses_random_subset(self):
        bank = self.bank('shuffled')
        original = list(bank.bank[0])
        with patch('torch.randperm', return_value=torch.tensor([2, 0, 4, 1, 3])) as randperm:
            bank.process_batch(torch.tensor([[[1., 0.]]]), [0], [0])
        randperm.assert_called_once_with(5)
        expected = torch.stack([original[i].feat for i in [2, 0, 4, 1]]).reshape(1, 4, 2)
        torch.testing.assert_close(bank.retrieval_blocks[0].context, expected)

    def test_short_history_and_off_keep_all_entries(self):
        for mode in ['cosine', 'shuffled', 'off']:
            bank = self.bank(mode)
            hist = bank.bank[0] if mode == 'off' else bank.bank[0][:3]
            self.assertIs(bank._select_history(hist, torch.ones(1, 1, 2), '', 0), hist)

    def test_cli_accepts_full_with_independent_retrieval_override(self):
        # Load only the parser to avoid importing simulator and TensorFlow.
        source = Path(__file__).resolve().parents[1] / 'evaluation/simpler_env/simpler_env_inference.py'
        tree = ast.parse(source.read_text())
        parser_fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'parse_local_args')
        namespace = {'argparse': argparse}
        exec(compile(ast.Module(body=[parser_fn], type_ignores=[]), str(source), 'exec'), namespace)
        for mode in ['cosine', 'shuffled']:
            args, remaining = namespace['parse_local_args']([
                '--experiment-mode', 'full', '--query-retrieval-mode', mode,
                '--query-retrieval-top-k', '4', '--robot', 'widowx'])
            self.assertEqual((args.experiment_mode, args.query_retrieval_mode, args.query_retrieval_top_k), ('full', mode, 4))
            self.assertEqual(remaining, ['--robot', 'widowx'])
        self.assertIsNone(namespace['parse_local_args']([])[0].query_retrieval_mode)


if __name__ == '__main__':
    unittest.main()

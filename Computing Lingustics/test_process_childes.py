"""Tests for the functions in process_childes.py.

Your task is to implement some test cases to increase our confidence in the correctness 
of the functions in process_childes.py.
"""
import os
import unittest

import process_childes as pc


class TestPrepareChildes(unittest.TestCase):
    """Tests for the functions in process_childes.py."""

    def test_process_unidentifiable(self):
        """Test the process_unidentifiable function."""
        self.assertEqual(pc.process_unidentifiable('xxx'), '<unk>')
        self.assertEqual(pc.process_unidentifiable('*CHI xxx yyy'), '*CHI <unk> <unk>')
        # TODO: write your test cases here
        # Added test cases
        self.assertEqual(pc.process_unidentifiable('xxxyyy'), 'xxxyyy')  # Not word-bounded
        self.assertEqual(pc.process_unidentifiable('www test'), '<unk> test')  # Different marker
        self.assertEqual(pc.process_unidentifiable('test xxx xxx'), 'test <unk> <unk>')  # Multiple

    def test_process_incomplete(self):
        """Test the process_incomplete function."""
        self.assertEqual(pc.process_incomplete('I been sit(ting) all day'), 'I been sitting all day')
        # TODO: write your test cases here
        # Added test cases
        self.assertEqual(pc.process_incomplete('walk(ing)'), 'walking')  # Simple case
        self.assertEqual(pc.process_incomplete('walk(ing) talk(ing)'), 'walking talking')  # Multiple
        self.assertEqual(pc.process_incomplete('(pre)fix'), 'prefix')  # Prefix incomplete

    def test_process_omit(self):
        """Test the process_omit function."""
        # TODO: write your test cases here
        pass

    def test_process_paralinguistic(self):
        """Test the process_paralinguistic function."""
        # TODO: write your test cases here
        # pass
        self.assertEqual(pc.process_paralinguistic("that's mine [=! cries]"), "that's mine")
        self.assertEqual(pc.process_paralinguistic("<that's mine> [=! cries]"), "that's mine")
        self.assertEqual(pc.process_paralinguistic('&=cries'), '')  # Only event
        self.assertEqual(
            pc.process_paralinguistic("<hello> [=! laughs] <there> [=! cries]"),
            "hello there"
        )  # Multiple events
        self.assertEqual(
            pc.process_paralinguistic('[! not paralinguistic]'),
            '[! not paralinguistic]'
        )  # Non-event bracket
        self.assertEqual(pc.process_omit('I want &=0to go'), 'I want go')
        self.assertEqual(pc.process_omit('&=0the cat'), 'cat')
        self.assertEqual(pc.process_omit('&=0the &=0a cat'), 'cat')  # Multiple omissions
        self.assertEqual(pc.process_omit('prefix&=0suffix'), 'prefix&=0suffix')  # No space
        self.assertEqual(pc.process_omit('&=0'), '')  # Empty case

    def test_complex(self):
        """Test some complex cases."""
        process_pipeline = lambda x: pc.process_paralinguistic(
            pc.process_omit(
                pc.process_incomplete(
                    pc.process_unidentifiable(x)
                )
            )
        )
        self.assertEqual(process_pipeline('xxx sit(ting) &=jumps www'), '<unk> sitting <unk>')
        # TODO: write your test cases here
        self.assertEqual(process_pipeline('xxx sit(ting) &=jumps www'), '<unk> sitting <unk>')
        # Added complex cases
        self.assertEqual(
            process_pipeline('xxx walk(ing) &=0the <run(ning)> [=! laughs]'),
            '<unk> walking running'
        )
        self.assertEqual(
            process_pipeline('&=0the xxx talk(ing) [=! cries] www'),
            '<unk> talking <unk>'
        )
        self.assertEqual(
            process_pipeline('<xxx> [=! crying] &=0to walk(ing)'),
            '<unk> walking'
        )
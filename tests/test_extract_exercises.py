#!/usr/bin/env python3
"""
Unit and integration tests for scripts/extract_exercises.py
"""

from pathlib import Path
import sys
import tempfile
import unittest

import fitz  # PyMuPDF

# Add scripts/ to Python path
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from extract_exercises import (
    COMBINED_FILENAME,
    DEFAULT_SOURCE_PATH,
    EXERCISE_CHAPTERS,
    ChapterMetadata,
    extract_chapter_exercise,
    extract_combined_workbook,
    main,
    run_extraction,
)


class TestExerciseMetadata(unittest.TestCase):
    """Test chapter definitions and page index ranges."""

    def test_chapter_list_and_ranges(self):
        expected = {
            2: ("Linear Algebra", 69, 74, 6, "Chapter_02_Linear_Algebra_Exercises.pdf"),
            3: ("Analytic Geometry", 101, 102, 2, "Chapter_03_Analytic_Geometry_Exercises.pdf"),
            4: ("Matrix Decompositions", 142, 143, 2, "Chapter_04_Matrix_Decompositions_Exercises.pdf"),
            5: ("Vector Calculus", 175, 176, 2, "Chapter_05_Vector_Calculus_Exercises.pdf"),
            6: ("Probability and Distributions", 227, 229, 3, "Chapter_06_Probability_and_Distributions_Exercises.pdf"),
            7: ("Continuous Optimization", 252, 253, 2, "Chapter_07_Continuous_Optimization_Exercises.pdf"),
        }

        self.assertEqual(len(EXERCISE_CHAPTERS), 6)
        total_pages = sum(meta.page_count for meta in EXERCISE_CHAPTERS)
        self.assertEqual(total_pages, 17)

        for meta in EXERCISE_CHAPTERS:
            self.assertIn(meta.chapter, expected)
            title, start, end, p_count, fname = expected[meta.chapter]
            self.assertEqual(meta.title, title)
            self.assertEqual(meta.start_page, start)
            self.assertEqual(meta.end_page, end)
            self.assertEqual(meta.page_count, p_count)
            self.assertEqual(meta.filename, fname)


class TestExtractionExecution(unittest.TestCase):
    """Test actual PDF extraction against the textbook."""

    @classmethod
    def setUpClass(cls):
        if not DEFAULT_SOURCE_PATH.is_file():
            raise unittest.SkipTest(f"Source PDF not found at {DEFAULT_SOURCE_PATH}")

    def test_full_extraction_to_tempdir(self):
        """Test complete extraction of all chapters and combined workbook."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            generated = run_extraction(
                source_path=DEFAULT_SOURCE_PATH,
                output_dir=out_dir,
                include_combined=True,
            )

            # 6 chapter files + 1 combined file = 7 files
            self.assertEqual(len(generated), 7)

            # Verify each individual chapter PDF
            expected_counts = {
                "Chapter_02_Linear_Algebra_Exercises.pdf": 6,
                "Chapter_03_Analytic_Geometry_Exercises.pdf": 2,
                "Chapter_04_Matrix_Decompositions_Exercises.pdf": 2,
                "Chapter_05_Vector_Calculus_Exercises.pdf": 2,
                "Chapter_06_Probability_and_Distributions_Exercises.pdf": 3,
                "Chapter_07_Continuous_Optimization_Exercises.pdf": 2,
            }

            for fname, expected_pages in expected_counts.items():
                pdf_path = out_dir / fname
                self.assertTrue(pdf_path.exists(), f"Missing file {fname}")
                doc = fitz.open(str(pdf_path))
                self.assertEqual(
                    len(doc),
                    expected_pages,
                    f"Wrong page count for {fname}: expected {expected_pages}, got {len(doc)}",
                )
                # Verify TOC is present
                toc = doc.get_toc()
                self.assertTrue(len(toc) >= 1)
                # Verify text contains 'Exercises'
                first_page_text = doc[0].get_text()
                self.assertIn("Exercises", first_page_text)
                doc.close()

            # Verify combined workbook
            combined_path = out_dir / COMBINED_FILENAME
            self.assertTrue(combined_path.exists())
            c_doc = fitz.open(str(combined_path))
            self.assertEqual(len(c_doc), 17)

            # Verify combined TOC structure
            toc = c_doc.get_toc()
            self.assertEqual(len(toc), 6)
            expected_toc_pages = [1, 7, 9, 11, 13, 16]
            for i, item in enumerate(toc):
                level, title, pageno = item
                self.assertEqual(level, 1)
                self.assertEqual(pageno, expected_toc_pages[i])
                self.assertIn(f"Chapter {EXERCISE_CHAPTERS[i].chapter}", title)
            c_doc.close()

    def test_single_chapter_filter(self):
        """Test extracting a single chapter via chapter filter."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            generated = run_extraction(
                source_path=DEFAULT_SOURCE_PATH,
                output_dir=out_dir,
                chapters=[3],
                include_combined=False,
            )

            self.assertEqual(len(generated), 1)
            pdf_path = out_dir / "Chapter_03_Analytic_Geometry_Exercises.pdf"
            self.assertTrue(pdf_path.exists())
            doc = fitz.open(str(pdf_path))
            self.assertEqual(len(doc), 2)
            doc.close()

    def test_combined_only_flag(self):
        """Test --combined-only flag generates only the combined workbook."""
        with tempfile.TemporaryDirectory() as tmpdir:
            out_dir = Path(tmpdir)
            generated = run_extraction(
                source_path=DEFAULT_SOURCE_PATH,
                output_dir=out_dir,
                combined_only=True,
            )

            self.assertEqual(len(generated), 1)
            self.assertEqual(generated[0].name, COMBINED_FILENAME)
            doc = fitz.open(str(generated[0]))
            self.assertEqual(len(doc), 17)
            doc.close()

    def test_cli_invocation(self):
        """Test invoking the script via CLI main() entrypoint."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ret = main(["--output-dir", tmpdir, "--chapters", "2", "--skip-combined"])
            self.assertEqual(ret, 0)
            self.assertTrue((Path(tmpdir) / "Chapter_02_Linear_Algebra_Exercises.pdf").exists())

    def test_invalid_source_file_error(self):
        """Test handling when source PDF does not exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(FileNotFoundError):
                run_extraction(
                    source_path=Path(tmpdir) / "nonexistent.pdf",
                    output_dir=Path(tmpdir),
                )


if __name__ == "__main__":
    unittest.main()

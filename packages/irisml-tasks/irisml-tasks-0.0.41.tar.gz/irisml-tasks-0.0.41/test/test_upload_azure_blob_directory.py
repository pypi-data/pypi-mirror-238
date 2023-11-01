import pathlib
import tempfile
import unittest
import unittest.mock

from irisml.tasks.upload_azure_blob_directory import Task


class TestUploadAzureBlobDirectory(unittest.TestCase):
    def test_simple(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_dir = pathlib.Path(temp_dir)
            (temp_dir / 'file1').write_text('file1')
            (temp_dir / 'file2').write_text('file2')
            (temp_dir / 'dir1').mkdir()
            (temp_dir / 'dir1' / 'file3').write_text('file3')
            (temp_dir / 'dir1' / 'dir2').mkdir()
            (temp_dir / 'dir1' / 'dir2' / 'file4').write_text('file4')
            with unittest.mock.patch('irisml.tasks.upload_azure_blob_directory.ContainerClient') as m_client:
                Task(Task.Config('https://fake_url/', temp_dir)).execute(Task.Inputs())
                m_client_instance = m_client.from_container_url.return_value
                self.assertEqual(m_client_instance.upload_blob.call_count, 4)

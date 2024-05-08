import cv2
import os
import glob
from langflow import CustomComponent
from langchain.schema import Document
from typing import Any, Dict, List


class ALLDirectoryLoaderComponent(CustomComponent):
    display_name: str = "All In One Directory Loader"
    description: str = "Recursively load components from a given directory"
    beta = True
    loaders_info: List[Dict[str, Any]] = [
    {
        "loader": "AirbyteJSONLoader",
        "name": "Airbyte JSON (.jsonl)",
        "import": "langchain.document_loaders.AirbyteJSONLoader",
        "defaultFor": ["jsonl"],
        "allowdTypes": ["jsonl"],
    },
    {
        "loader": "JSONLoader",
        "name": "JSON (.json)",
        "import": "langchain.document_loaders.JSONLoader",
        "defaultFor": ["json"],
        "allowdTypes": ["json"],
    },
    {
        "loader": "BSHTMLLoader",
        "name": "BeautifulSoup4 HTML (.html, .htm)",
        "import": "langchain.document_loaders.BSHTMLLoader",
        "allowdTypes": ["html", "htm"],
    },
    {
        "loader": "CSVLoader",
        "name": "CSV (.csv)",
        "import": "langchain.document_loaders.CSVLoader",
        "defaultFor": ["csv"],
        "allowdTypes": ["csv"],
    },
    {
        "loader": "CoNLLULoader",
        "name": "CoNLL-U (.conllu)",
        "import": "langchain.document_loaders.CoNLLULoader",
        "defaultFor": ["conllu"],
        "allowdTypes": ["conllu"],
    },
    {
        "loader": "EverNoteLoader",
        "name": "EverNote (.enex)",
        "import": "langchain.document_loaders.EverNoteLoader",
        "defaultFor": ["enex"],
        "allowdTypes": ["enex"],
    },
    {
        "loader": "FacebookChatLoader",
        "name": "Facebook Chat (.json)",
        "import": "langchain.document_loaders.FacebookChatLoader",
        "allowdTypes": ["json"],
    },
    {
        "loader": "OutlookMessageLoader",
        "name": "Outlook Message (.msg)",
        "import": "langchain.document_loaders.OutlookMessageLoader",
        "defaultFor": ["msg"],
        "allowdTypes": ["msg"],
    },
    {
        "loader": "PyPDFLoader",
        "name": "PyPDF (.pdf)",
        "import": "langchain.document_loaders.PyPDFLoader",
        "defaultFor": ["pdf"],
        "allowdTypes": ["pdf"],
    },
    {
        "loader": "STRLoader",
        "name": "Subtitle (.str)",
        "import": "langchain.document_loaders.STRLoader",
        "defaultFor": ["str"],
        "allowdTypes": ["str"],
    },
    {
        "loader": "TextLoader",
        "name": "Text (.txt)",
        "import": "langchain.document_loaders.TextLoader",
        "defaultFor": ["txt"],
        "allowdTypes": ["txt"],
    },
    {
        "loader": "UnstructuredEmailLoader",
        "name": "Unstructured Email (.eml)",
        "import": "langchain.document_loaders.UnstructuredEmailLoader",
        "defaultFor": ["eml"],
        "allowdTypes": ["eml"],
    },
    {
        "loader": "UnstructuredHTMLLoader",
        "name": "Unstructured HTML (.html, .htm)",
        "import": "langchain.document_loaders.UnstructuredHTMLLoader",
        "defaultFor": ["html", "htm"],
        "allowdTypes": ["html", "htm"],
    },
    {
        "loader": "UnstructuredMarkdownLoader",
        "name": "Unstructured Markdown (.md)",
        "import": "langchain.document_loaders.UnstructuredMarkdownLoader",
        "defaultFor": ["md"],
        "allowdTypes": ["md"],
    },
    {
        "loader": "UnstructuredPowerPointLoader",
        "name": "Unstructured PowerPoint (.pptx)",
        "import": "langchain.document_loaders.UnstructuredPowerPointLoader",
        "defaultFor": ["pptx"],
        "allowdTypes": ["pptx"],
    },
    {
        "loader": "UnstructuredWordLoader",
        "name": "Unstructured Word (.docx)",
        "import": "langchain.document_loaders.UnstructuredWordLoader",
        "defaultFor": ["docx"],
        "allowdTypes": ["docx"],
    },
    {
        "loader": "UnstructuredEPubLoader",
        "name": "Unstructured EPub (.epub)",
        "import": "langchain.document_loaders.UnstructuredEPubLoader",
        "defaultFor": ["epub"],
        "allowdTypes": ["epub"],
    },
    {
        "loader": "UnstructuredImageLoader",
        "name": "Unstructured Image (.jpg, .png, .jpeg)",
        "import": "langchain_community.document_loaders.image.UnstructuredImageLoader",
        "defaultFor": ["jpg","png","jpeg"],
        "allowdTypes": ["jpg","png","jpeg"],
    },
]

    def build_config(self):
        loader_options = ["Automatic"] + [
            loader_info["name"] for loader_info in self.loaders_info
        ]

        file_types = []
        suffixes = []

        for loader_info in self.loaders_info:
            if "allowedTypes" in loader_info:
                file_types.extend(loader_info["allowedTypes"])
                suffixes.extend([f".{ext}" for ext in loader_info["allowedTypes"]])

        return {
            "file_path": {
                "display_name": "File Path",
                "required": True,
                "field_type": "file",
                "file_types": [
                    "json",
                    "txt",
                    "csv",
                    "jsonl",
                    "html",
                    "htm",
                    "conllu",
                    "enex",
                    "msg",
                    "pdf",
                    "srt",
                    "eml",
                    "md",
                    "pptx",
                    "docx",
                    "docx",
                    "epub",
                    "jpg",
                    "jpeg",
                    "png",
                ],
                "suffixes": [
                    ".json",
                    ".txt",
                    ".csv",
                    ".jsonl",
                    ".html",
                    ".htm",
                    ".conllu",
                    ".enex",
                    ".msg",
                    ".pdf",
                    ".srt",
                    ".eml",
                    ".md",
                    ".pptx",
                    ".docx",
                    ".epup",
                    ".jpg",
                    ".jpeg",
                    ".png",
                ],
                # "file_types" : file_types,
                # "suffixes": suffixes,
            },
            "loader": {
                "display_name": "Loader",
                "is_list": True,
                "required": True,
                "options": loader_options,
                "value": "Automatic",
            },
        }

    def load_file(self, file_path: str, loader: str):
        file_type = file_path.split(".")[-1]

        selected_loader_info = None
        for loader_info in self.loaders_info:
            if loader_info["name"] == loader:
                selected_loader_info = loader_info
                break

        if selected_loader_info is None and loader != "Automatic":
            raise ValueError(f"Loader {loader} not found in the loader info list")

        if loader == "Automatic":
            default_loader_info = None
            for info in self.loaders_info:
                if "defaultFor" in info and file_type in info["defaultFor"]:
                    default_loader_info = info
                    break

            if default_loader_info is None:
                raise ValueError(f"No default loader found for file type: {file_type}")

            selected_loader_info = default_loader_info
        if isinstance(selected_loader_info, dict):
            loader_import: str = selected_loader_info["import"]
        else:
            raise ValueError(
                f"Loader info for {loader} is not a dict\nLoader info:\n{selected_loader_info}"
            )
        module_name, class_name = loader_import.rsplit(".", 1)

        try:
            loader_module = __import__(module_name, fromlist=[class_name])
            loader_instance = getattr(loader_module, class_name)
        except ImportError as e:
            raise ValueError(
                f"Loader {loader} could not be imported\nLoader info:\n{selected_loader_info}"
            ) from e

         # Set extract_images to True only for PDF or DOCX loaders
        if file_type in ["pdf", "docx"]:
            result = loader_instance(file_path=file_path, extract_images=True)
        else:
            result = loader_instance(file_path=file_path)
        result = result.load()
        self.status = result
        return result
        
    def recursive_glob(self, directory_path, depth):
        pattern = "/**/*.*" if depth > 0 else "/*.*"
        return [file for file in glob.glob(directory_path + pattern, recursive=True) if file.count(os.sep) <= depth + directory_path.count(os.sep)]
    

    def build(self, directory_path: str, loader: str, depth:int=3) -> Document:
        if not os.path.exists(directory_path):
            raise ValueError(f"Directory not found: {directory_path}")
            
        suffixes = list(set([i for j in self.loaders_info for i in j["allowdTypes"]]))

        files = self.recursive_glob(directory_path, depth=depth)
        files = [f for f in files if f.split('.')[-1] in suffixes]
        
        docs = []
        for file in files:
            doc = self.load_file(file, loader)
            docs.extend(doc)
        self.status = docs
        return docs
            
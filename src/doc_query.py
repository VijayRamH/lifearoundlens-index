################################################################
# Derived class for defining access to reading PDF documents
################################################################ 

class DocQuery():
    document        =   ""
    ver             =   "1.0"
    type            =   "pdf"
    data            =   ""
    chunk           =   ""
    chunk_size      =   256
    chunk_overlap   =   0

    #-----------------------------------------------------------
    # CTOR - loads the document and validates it for known 
    # filetypes and chunks it to be ready for embedding
    #-----------------------------------------------------------
    def __init__(self, document):
        self.document = document

        import os
        name, file_extension = os.path.splitext(document)

        if file_extension == '.pdf':
            #load the pdf document
            from langchain.document_loaders import PyPDFLoader
            print(f"Loading pdf file {self.document} ...")
            loader      = PyPDFLoader(document)
            self.data   = loader.load()
        elif file_extension == '.docx':
            #load .docx files
            from langchain.document_loaders import Docx2txtLoader
            print(f"Loading docx file {self.document} ...")
            loader      =   Docx2txtLoader(document)
            self.data   =   loader.load()
        else:
            print("Document not supported ...")
            return None    
        
        #chunk the pdf document
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        text_splitter   = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        self.chunks     = text_splitter.split_documents(self.data)
    
    #-----------------------------------------------------------
    #Debug method
    #-----------------------------------------------------------
    def version(self):
        print(f"DocQuery class version ({self.ver})")

    #-----------------------------------------------------------
    #Debug method
    #-----------------------------------------------------------
    def printVars(self):
        print(f"DocQuery processing document {self.document}")
        print(f"DocQuery no of document pages",len(self.data))

    #-----------------------------------------------------------
    #Debug method
    #-----------------------------------------------------------
    def printPage(self,pg_index):
        print(f"DocQuery page content for {pg_index} is {self.data[pg_index].metadata}")

    #-----------------------------------------------------------
    #Getter method for chunk data
    #-----------------------------------------------------------
    def getDocumentChunks(self):
        return self.chunks        

################################################################
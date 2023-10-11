# pylint: disable=E0633
import sys

import PyPDF2
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class PDFMerger:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.window = QMainWindow()
        self.window.setWindowTitle("PDF Merger")
        self.central_widget = QWidget()
        self.layout = QVBoxLayout()

        self.label = QLabel("Selecione os PDFs para anexar:")
        self.layout.addWidget(self.label)

        self.button = QPushButton("Anexar PDFs")
        self.button.clicked.connect(self.merge_pdfs)
        self.layout.addWidget(self.button)

        self.central_widget.setLayout(self.layout)
        self.window.setCentralWidget(self.central_widget)

    def run(self):
        self.window.show()
        sys.exit(self.app.exec())

    def merge_pdfs(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_paths, _ = QFileDialog.getOpenFileNames(
            self.window,
            "Selecionar PDFs",
            "",
            "PDF Files (*.pdf);;All Files (*)",
            options=options,
        )

        if file_paths:
            # Crie um novo arquivo PDF resultante
            merged_pdf = PyPDF2.PdfWriter()

            for file_path in file_paths:
                pdf = open(file_path, "rb")
                pdf_reader = PyPDF2.PdfReader(pdf)

                # Anexe páginas do PDF atual ao PDF resultante
                for page in pdf_reader.pages:
                    merged_pdf.add_page(page)

                pdf.close()

            # Salve o PDF resultante
            output_file, _ = QFileDialog.getSaveFileName(  # type: ignore
                self.window,
                "Salvar PDF Anexado",
                "",
                "PDF Files (*.pdf);;All Files (*)",
                options=options,
            )
            if output_file:
                with open(output_file, "wb") as result_pdf:
                    merged_pdf.write(result_pdf)

                self.label.setText("PDFs anexados com sucesso!")
            else:
                self.label.setText("Operação cancelada.")
        else:
            self.label.setText("Nenhum PDF selecionado.")


if __name__ == "__main__":
    pdf_merger = PDFMerger()
    pdf_merger.run()

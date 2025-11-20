import platform
import os
import asyncio
from fastapi import HTTPException
from app_logging import logger

async def convert_docx_to_pdf(docx_path):
    """ Converts DOCX to PDF using LibreOffice (Linux) or Microsoft Word (Windows). """
    pdf_path = docx_path.replace(".docx", ".pdf")

    try:
        if platform.system() == "Windows":
            import win32com.client
            word = win32com.client.Dispatch("Word.Application")
            doc = word.Documents.Open(os.path.abspath(docx_path))
            doc.SaveAs(os.path.abspath(pdf_path), FileFormat=17)  # PDF format
            doc.Close()
            word.Quit()
            # print(f" Converted {docx_path} to {pdf_path} using Microsoft Word")
            logger.info("Converted %s to %s using Microsoft Word", docx_path, pdf_path)
        else:
            libreoffice_path = "/usr/bin/libreoffice"
            if not os.path.exists(libreoffice_path):
                raise FileNotFoundError(f"LibreOffice not found at {libreoffice_path}")

            process = await asyncio.create_subprocess_exec(
                libreoffice_path, "--headless", "--convert-to", "pdf",
                "--outdir", os.path.dirname(docx_path), docx_path
            )
            await process.communicate()  # Ensure subprocess completes
            logger.info("Converted %s to %s using LibreOffice", docx_path, pdf_path)
            # print(f" Converted {docx_path} to {pdf_path} using LibreOffice")

        return pdf_path
    except Exception as e:
        # print(f" DOCX to PDF conversion failed: {e}")
        logger.error("DOCX to PDF conversion failed: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"DOCX to PDF conversion failed: {e}")
from datetime import datetime
from decimal import Decimal
from service.transactionService import service as transaction_service

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors

from io import BytesIO

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

class GeneratorReportService:
    async def generate_report(self, sender_id: int):
        pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))
        pdfmetrics.registerFont(TTFont('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'))

        transactions = await transaction_service.get_transactions_by_sender_id(sender_id)

        total_income = Decimal('0.00')
        total_expenses = Decimal('0.00')
        transaction_data = []

        transaction_data.append(["ID", "Сумма", "Валюта", "Тип", "Описание", "Категория", "Дата"])

        for transaction in transactions:
            amount = Decimal(str(transaction["amount"]))
            transaction_type = "Н/Д"

            if transaction["receiverId"] == sender_id:
                total_income += amount
                transaction_type = "Доход"
            elif transaction["senderId"] == sender_id:
                total_expenses += amount
                transaction_type = "Расход"

            category_name = transaction["category"]["name"] if transaction.get("category") else "Н/Д"
            created_at = datetime.fromisoformat(transaction["createdAt"]).strftime("%Y-%m-%d %H:%M:%S")

            transaction_data.append([
                str(transaction["id"]),
                f"{amount:.2f}",
                transaction["currency"],
                transaction_type,
                transaction["description"],
                category_name,
                created_at
            ])

        file_name = f"report_{sender_id}.pdf"
        doc = SimpleDocTemplate(file_name, pagesize=letter)
        styles = getSampleStyleSheet()

        styles.add(ParagraphStyle(name='ReportTitle',
                                  fontName='DejaVuSans',
                                  fontSize=24,
                                  leading=28,
                                  alignment=1,
                                  spaceAfter=20))

        styles.add(ParagraphStyle(name='SectionHeader',
                                  fontName='DejaVuSans',
                                  fontSize=16,
                                  leading=18,
                                  spaceAfter=10,
                                  textColor=colors.darkblue))

        styles.add(ParagraphStyle(name='NormalRus',
                                  fontName='DejaVuSans',
                                  fontSize=10,
                                  leading=12))

        styles['h2'].fontName = 'DejaVuSans'

        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []

        story.append(Paragraph("Финансовый отчет для пользователя", styles['ReportTitle']))
        story.append(Spacer(1, 0.3 * inch))

        story.append(Paragraph("Финансовая сводка:", styles['SectionHeader']))
        story.append(Paragraph(f"Общий доход: <font color='green'>${total_income:.2f}</font>", styles['h2'])) 
        story.append(Paragraph(f"Общие расходы: <font color='red'>${total_expenses:.2f}</font>", styles['h2']))
        story.append(Spacer(1, 0.5 * inch))

        if len(transaction_data) > 1:
            story.append(Paragraph("Детали транзакций:", styles['SectionHeader']))
            story.append(Spacer(1, 0.2 * inch))

            col_widths = [2.7*inch, 0.6*inch, 0.7*inch, 0.6*inch, 1.0*inch, 1.0*inch, 1.5*inch]
            table = Table(transaction_data, colWidths=col_widths)

            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'DejaVuSans-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#E8F5E9')),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#A5D6A7')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
                ('FONTSIZE', (0,1), (-1,-1), 9),
                ('FONTNAME', (0,1), (-1,-1), 'DejaVuSans'),
            ]))
            story.append(table)
        else:
            story.append(Paragraph("Транзакции для этого пользователя не найдены.", styles['NormalRus']))

        try:
            doc.build(story)
            buffer.seek(0)
            return {
                "content": buffer.getvalue(),
                "filename": f"financial_report_{sender_id}.pdf"
            }
        except Exception as e:
            return {"error": str(e)}
        finally:
            buffer.close()
        
service = GeneratorReportService()
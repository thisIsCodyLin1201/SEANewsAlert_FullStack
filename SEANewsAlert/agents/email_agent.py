"""
Email Agent
負責透過 SMTP 發送郵件（使用 MCP Email 概念）
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path
from typing import List, Union
from config import Config
from datetime import datetime


class EmailAgent:
    """郵件代理 - 負責發送報告郵件"""
    
    def __init__(self):
        """初始化 Email Agent"""
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.email_address = Config.EMAIL_ADDRESS
        self.email_password = Config.EMAIL_PASSWORD
    
    def send_report(
        self,
        recipients: Union[str, List[str]],
        pdf_path: Path,
        excel_path: Path = None,
        subject: str = None,
        body: str = None
    ) -> bool:
        """
        發送報告郵件
        
        Args:
            recipients: 收件人郵箱地址（字串或列表）
            pdf_path: PDF 報告路徑
            excel_path: Excel 報告路徑（可選）
            subject: 郵件主題（可選）
            body: 郵件內容（可選）
            
        Returns:
            bool: 發送是否成功
        """
        print("📧 Email Agent 開始發送郵件...")
        
        # 處理收件人格式
        if isinstance(recipients, str):
            recipients = [r.strip() for r in recipients.split(',')]
        
        # 設置預設主題和內容
        if not subject:
            subject = f"【{Config.APP_NAME}】東南亞金融新聞報告 - {datetime.now().strftime('%Y-%m-%d')}"
        
        if not body:
            body = self._generate_email_body(pdf_path, excel_path)
        
        try:
            # 創建郵件
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = subject
            
            # 添加郵件內容
            msg.attach(MIMEText(body, 'html', 'utf-8'))
            
            # 添加 PDF 附件
            if pdf_path.exists():
                with open(pdf_path, 'rb') as f:
                    pdf_attachment = MIMEApplication(f.read(), _subtype='pdf')
                    pdf_attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=pdf_path.name
                    )
                    msg.attach(pdf_attachment)
            else:
                raise FileNotFoundError(f"PDF 文件不存在: {pdf_path}")
            
            # 添加 Excel 附件（如果提供）
            if excel_path and excel_path.exists():
                with open(excel_path, 'rb') as f:
                    excel_attachment = MIMEApplication(
                        f.read(), 
                        _subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                    )
                    excel_attachment.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=excel_path.name
                    )
                    msg.attach(excel_attachment)
                print(f"✅ 已添加 Excel 附件: {excel_path.name}")
            
            # 連接 SMTP 服務器並發送
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # 啟用 TLS 加密
                server.login(self.email_address, self.email_password)
                server.send_message(msg)
            
            print(f"✅ 郵件發送成功！收件人: {', '.join(recipients)}")
            return True
            
        except Exception as e:
            print(f"❌ 郵件發送失敗: {str(e)}")
            return False
    
    def _generate_email_body(self, pdf_path: Path, excel_path: Path = None) -> str:
        """生成郵件內容（HTML 格式）"""
        
        # 計算附件資訊
        attachments_info = f"""
                        <li><strong>PDF 報告</strong>：{pdf_path.name} ({pdf_path.stat().st_size / 1024:.2f} KB)</li>
        """
        
        if excel_path and excel_path.exists():
            attachments_info += f"""
                        <li><strong>Excel 數據表</strong>：{excel_path.name} ({excel_path.stat().st_size / 1024:.2f} KB)</li>
            """
        
        return f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: "Microsoft JhengHei", Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                }}
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    background-color: #1a5490;
                    color: white;
                    padding: 20px;
                    text-align: center;
                    border-radius: 5px 5px 0 0;
                }}
                .content {{
                    background-color: #f9f9f9;
                    padding: 20px;
                    border: 1px solid #ddd;
                }}
                .footer {{
                    background-color: #f0f0f0;
                    padding: 15px;
                    text-align: center;
                    font-size: 12px;
                    color: #666;
                    border-radius: 0 0 5px 5px;
                }}
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #1a5490;
                    color: white;
                    text-decoration: none;
                    border-radius: 5px;
                    margin-top: 10px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🌏 {Config.APP_NAME}</h1>
                </div>
                <div class="content">
                    <h2>親愛的用戶，您好！</h2>
                    <p>感謝您使用我們的服務。您請求的東南亞金融新聞報告已經生成完成。</p>
                    
                    <h3>📎 附件清單</h3>
                    <ul>
{attachments_info}
                        <li><strong>生成時間</strong>：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</li>
                    </ul>
                    
                    <h3>📋 報告內容</h3>
                    <p>本報告包含最新的東南亞金融市場動態，涵蓋主要國家的經濟新聞和市場分析。</p>
                    
                    <p><strong>附件說明：</strong></p>
                    <ul>
                        <li>📄 <strong>PDF 報告</strong>：完整的新聞分析報告，包含詳細摘要和市場洞察</li>
                        {"<li>📊 <strong>Excel 數據表</strong>：結構化的新聞清單，便於進一步分析和處理</li>" if excel_path and excel_path.exists() else ""}
                    </ul>
                    
                    <p style="margin-top: 20px;">
                        <strong>溫馨提示</strong>：如有任何問題，請隨時與我們聯繫。
                    </p>
                </div>
                <div class="footer">
                    <p>本郵件由 {Config.APP_NAME} v{Config.APP_VERSION} 自動生成</p>
                    <p>© 2025 All Rights Reserved</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    def test_connection(self) -> bool:
        """測試郵件服務器連接"""
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port, timeout=10) as server:
                server.starttls()
                server.login(self.email_address, self.email_password)
            print("✅ 郵件服務器連接成功")
            return True
        except Exception as e:
            print(f"❌ 郵件服務器連接失敗: {str(e)}")
            return False


if __name__ == "__main__":
    # 測試 Email Agent
    agent = EmailAgent()
    
    # 測試連接
    agent.test_connection()

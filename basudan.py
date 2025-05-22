import requests

def send_invoice_file_template(to, template_name, language, parameters, api_url="http://89.250.65.247:8888/send_template_message"):
    """
    Send a WhatsApp template message for invoice file using the specified API endpoint.
    Args:
        to (str): Recipient phone number (in international format)
        template_name (str): Name of the WhatsApp template
        language (str): Language code (e.g., 'ar')
        parameters (list): List of template parameters (str)
        api_url (str): The API endpoint URL
    Returns:
        dict: API response as a dictionary
    """
    payload = {
        "to": to,
        "template_name": template_name,
        "language": language,
        "parameters": parameters
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(api_url, json=payload, headers=headers)
    try:
        return response.json()
    except Exception:
        return {"status": "error", "message": "Invalid response", "raw": response.text}
    
def send_invoice_with_file(
        customer_phone,
        name,
        invoice_number,
        amount,
        currency,
        file_path,
        api_url="http://89.250.65.247:8888/send-invoice"
    ):
        """
        Send an invoice with a PDF file using multipart/form-data.

        Args:
            customer_phone (str): Recipient phone number (in international format)
            name (str): Customer name
            invoice_number (str): Invoice number
            amount (str or int): Invoice amount
            currency (str): Currency code (e.g., 'SAR')
            file_path (str): Path to the PDF file
            api_url (str): The API endpoint URL

        Returns:
            dict: API response as a dictionary
        """
        data = {
            "customer_phone": customer_phone,
            "name": name,
            "invoice_number": invoice_number,
            "amount": str(amount),
            "currency": currency
        }
        files = {
            "file": open(file_path, "rb")
        }
        try:
            response = requests.post(api_url, data=data, files=files)
            return response.json()
        except Exception:
            return {"status": "error", "message": "Invalid response", "raw": response.text}
        finally:
            files["file"].close()

# Example usage:
if __name__ == "__main__":
    # result = send_invoice_file_template(
    #     to="966504677306",
    #     template_name="invoice_file_send2",
    #     language="ar",
    #     parameters=[
    #         "محمد",
    #         "شركة المجد المشرق للتجارة",
    #         "1010320",
    #         "https://NewPoent.com/vo4lan3ccb.pdf"
    #     ]
    # )
    # print(result)

    result2 = send_invoice_with_file(
            customer_phone="966504677306",
            name="أحمد محمد",
            invoice_number="INV-2023-456",
            amount=750,
            currency="SAR",
            file_path="/home/mr-mohamed/Downloads/pdf/aktshf-mtah-altalm.pdf"
        )
    print(result2)
    # Example usage:
        
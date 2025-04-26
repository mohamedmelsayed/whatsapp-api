from pywa import WhatsApp
import os

wa = WhatsApp(
    phone_id=os.getenv("WHATSAPP_PHONE_NUMBER_ID"),
    token=os.getenv("WHATSAPP_ACCESS_TOKEN")
)



wa.send_message(
    to='96899839152',
    text='Hi this is Eng.Mohamed From Rawasy Alitqan ! This message sent from whatsapp api python code!'
)

wa.send_image(
    to='96899839152',
    image='https://www.rd.com/wp-content/uploads/2021/04/GettyImages-1053735888-scaled.jpg'
)

# doc_id=wa.upload_media(
# mime_type='application/pdf',


#     media='/home/mr-mohamed/Downloads/pdf/aktshf-mtah-altalm.pdf',

#     filename='aktshf-mtah-altalm.pdf',

# )

# echo doc_id
print(doc_id)   

wa.send_document(
    to="96899839152",
    # document=doc_id,
    document="1822582625191022",
    filename="aktshf-mtah-altalm.pdf",
    caption="aktshf-mtah-altalm.pdf"
)
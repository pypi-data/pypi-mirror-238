# Importing packages

import crcmod
import qrcode


# Copy and Paste function

def CopiaCola(pix_key: str, amount: float, name: str, data_field: str = "pyx-by-mksDEV08", merchant_category_code: str = "0000",
              transaction_currency: str = "986", city: str = "SAO PAULO", postal_code: str = "05409000"):
    # Define Header

    header = "00020126580014BR.GOV.BCB.PIX"

    # Define Pix Key

    if len(pix_key) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        pix_key = f"01{len(pix_key)}{pix_key}"

    else:
        pix_key = f"010{len(pix_key)}{pix_key}"

    # Define Merchant Category Code (Only for business)

    if len(merchant_category_code) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        merchant_category_code = f"52{len(merchant_category_code)}{merchant_category_code}"

    else:
        merchant_category_code = f"520{len(merchant_category_code)}{merchant_category_code}"

    # Define Transaction Currency Code (986 by default for BRL)

    if len(transaction_currency) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        transaction_currency = f"53{len(transaction_currency)}{transaction_currency}"

    else:
        transaction_currency = f"530{len(transaction_currency)}{transaction_currency}"

    # Define Amount

    amount = f"{amount:.2f}"
    if len(amount) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        amount = f"54{len(amount)}{amount}"

    else:
        amount = f"540{len(amount)}{amount}"

    #

    country_code = "5802BR"  # Define Country Code (BR by default)

    # Define Name (Bank account Name)

    if len(name) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        name = f"59{len(name)}{name}"

    else:
        name = f"590{len(name)}{name}"

    # Define City (by default SAO PAULO)

    if len(city) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        city = f"60{len(city)}{city}"

    else:
        city = f"600{len(city)}{city}"

    #

    postal_code = f"6108{postal_code}"  # Define postal code (05409000 by default for SAO PAULO)

    # Define Data Field (Optional free field to identify transactions)

    if len(data_field) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        data_field = f"05{len(data_field)}{data_field}"

    else:
        data_field = f"050{len(data_field)}{data_field}"

    if len(data_field) > 9:  # Conditional to check if var is > 9 and if not add a 0 before the var
        data_field = f"05{len(data_field)}{data_field}"

    else:
        data_field = f"050{len(data_field)}{data_field}"

    crc16 = "6304"  # Define CRC16 payload

    pixPayload = f"{header}{pix_key}{merchant_category_code}{transaction_currency}{amount}{country_code}{name}{city}" \
                 f"{postal_code}{data_field}{crc16}"  #

    # Encrypt Pix Payload

    def crc16Gen(payload):
        crc = crcmod.mkCrcFun(poly=0x11021, initCrc=0xFFFF, rev=False, xorOut=0x0000)
        crc16Code = hex(crc(str(payload).encode('utf-8')))
        formatCrc16Code = str(crc16Code).replace('0x', '').upper()

        return formatCrc16Code

    return pixPayload + crc16Gen(pixPayload)


def QrCode(pix_key: str, amount: float, name: str, data_field: str, file_name: str,
           merchant_category_code: str = "0000", transaction_currency: str = "986", city: str = "SAO PAULO",
           postal_code: str = "05409000", format: str = "png", create_file: bool = True):
    qr = qrcode.make(CopiaCola(pix_key, amount, name, data_field, merchant_category_code, transaction_currency, city,
                               postal_code))

    if create_file:
        qr.save(f"{file_name}.{format}")

    else:
        return qr

# UAE bank list: sources

`uae_hr/setup/uae_banks.csv` seeds the **UAE Bank** list on install and every migrate, insert-only by IBAN bank
code: a code or bank name already on a site is never overwritten.

**The IBAN bank code** is characters 5 to 7 of a UAE IBAN (`AEkk BBB AAAAAAAAAAAAAAAA`): `AE`, two check digits,
three bank-code digits, then the 16-digit account. The 9-digit WPS routing code carries the same three digits in
positions 2 to 4, which every seeded row satisfies.

## What is seeded

Only rows where the IBAN code agrees in at least two independent lists or on the bank's own published page
("verified"). Routing codes are filled only where the sources agree on one; several banks use a routing code per
branch, so blank means "ask your WPS agent", not "none". Banks that have merged are kept, **disabled**, with the
surviving bank in the notes, so old IBANs still decode: an Employee IBAN from one of them is warned.

Not seeded, because only one secondary source gives them: 001 Central Bank of the UAE, 010 Bank Melli Iran,
013 Bank Saderat Iran, 037 National Bank of Dubai (legacy), 043 Industrial and Commercial Bank of China,
048 Emirates Investment Bank, 092 Gulf International Bank, 093 Intesa Sanpaolo. No code was found for Zand or
Reem. Add them on your site once your WPS agent confirms them; a later release can add them here with a source.

## Sources (checked October 2026)

- HSBC UAE, "List of beneficiary bank codes for AutoPay services" (2022):
  https://www.business.hsbc.ae/-/media/library/markets-selective/uae/pdf/list-of-beneficiary-bank-codes-for-autopay-services.pdf
- Emirates Islamic, "Business Online salary and WPS file creation user guide" (2021):
  https://www.emiratesislamic.ae/-/media/ei/pdfs/business-online/salary-and-utility-payments/ei_businessonline_salary_wps_file_creation_user_guide.pdf
- Commercial Bank of Dubai, WPS user guide: https://www.cbd.ae/docs/librariesprovider2/payments_downloads/wps---user-guide.pdf
- RAKBANK SWIFT codes page: https://www.rakbank.ae/en/everyday-banking/send-pay/swiftcodes-remittances
- Standard Chartered UAE IBAN FAQ: https://www.sc.com/ae/iban/faq/
- Wio Bank salary page: https://wio.io/salary-plan
- Mbank (Al Maryah Community Bank): https://www.mbank.ae/about/
- National Bank of Fujairah contact page (routing code): https://nbf.ae/en/contact/get-in-touch
- Ruya Bank salary page (routing code): https://ruyabank.ae/en/salary
- The banks' own websites for 035, 033, 026, 024, 050, 023, 038, 012, 046, 057, 022, 042, 008, 034, 053, 021, 020,
  011, 029, 056, 054 (SWIFT and routing match).
- Central Bank of the UAE register of licensed financial institutions (August 2026), for current names and for
  which banks no longer operate.

Mbank publishes `E097AEXX` as its local identifier; it is not an 8-character SWIFT, so the SWIFT field is blank.
Ruya Bank's SWIFT was not confirmed and is blank.

Found an error? Open an issue with the bank's own published source.

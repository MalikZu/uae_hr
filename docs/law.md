# UAE private-sector labour law: the rules UAE HR is built on

> **Not legal advice.** This is a working extract made to build software, not a legal opinion. The quotes are
> from MOHRE's official English text; **the Arabic text prevails** (DL 66), and the Cabinet may change any period,
> percentage or value (DL 70(7)). Check anything that matters against the current Arabic text and with a
> qualified adviser. Corrections are welcome: open an issue with the article number and the source.

Every number the app uses comes from this file and lives in `uae_hr/law.py` with its citation. A test checks that
each quote in `law.py` appears here word for word.

**Source:** MOHRE official English booklet "Federal Decree-Law No. (33) of 2021 Regarding the Regulation of Employment Relationships and its amendments" + "Cabinet Resolution No. (1) of 2022 On the Implementation of Federal Decree-Law No. (33) of 2021" (PDF created 2025-10-16, downloaded 2026-10-15 from mohre.gov.ae).

**Notation:** DL = Federal Decree-Law 33/2021. CR = Cabinet Resolution 1/2022 (Implementing Regulation). `DL 9(1)` = Article 9, Clause 1; `DL 25(1)(f)` = Article 25, Clause 1, item f.
**Method:** every number below was read from the booklet text (pdftotext, and page images where the PDF text layer was garbled: DL 13, 29(3)–(10), 32(3)–38, 39–42, 43, 59–65). Quotes are verbatim, including the booklet's own spelling and grammar. Nothing has been added from memory. Where the English is odd or contradictory, the row says **AMBIGUOUS**.
**In force:** DL "shall be enforced as of 2 February 2022" (DL 74); CR "shall come into force as of 02 February 2022" (CR 39).

**Definitions every calculation depends on (DL 1):**
- **Basic Wage:** "paid to the worker in consideration of his work … and which does not include any other allowances or benefits in-kind."
- **Wage:** "The basic wage, in addition to the cash allowances and benefits in-kind allocated to the worker". It may include in-kind benefits or their cash equivalent, effort and risk allowances, cost-of-living allowances, and a percentage of sales or profits.
- **Continuous Service:** "Uninterrupted service with the same employer or its legal successor, from the date of commencement of work."
- **Worker's Family:** "Spouse, sons and daughters." **Juvenile:** 15 years or older and not yet over 18. **Day Worker:** "Each worker receiving a daily wage."

Which wage base each payment uses is shown in the Parameters column (basic wage vs wage vs last wage). The difference matters.

---

## 1. Employment contract

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 8(1) | Written contract in the agreed work pattern, on the Ministry form, in two copies: one kept by the employer, one handed to the worker. | 2 copies | "The contract shall be made in two copies; one copy shall be kept by the employer and the other shall be handed over to the worker" |
| DL 8(2) | The worker may prove the contract, the wage and his rights "by all possible means of proof". | none | "The worker or his representative may prove by all possible means of proof the employment contract, the amount of the wage" |
| DL 8(3) **AMENDED** (Federal Decree-Law No. (14) of 2022) | Contracts are fixed-term and renewable by agreement. **The amended text sets no maximum duration and no limit on the number of renewals.** | Max term: not stated. Renewals: by agreement of both parties | "Contract of employment shall be concluded for a specified period of time, subject to renewal, in accordance with the agreement of both parties." |
| DL 8(4) | An extension or renewal is added to the original term when counting continuous service. | Renewals count toward continuous service | "the new term(s) shall be considered an extension of the original term and shall be added to it while calculating the worker's continuous term of service" |
| DL 8(5) | If both parties keep performing after expiry without an express agreement, the contract is implicitly extended on the same terms. | none | "the original contract is considered implicitly extended as per the same conditions set forth therein." |
| CR 10(1) | Mandatory contract contents. | Fields: employer name and address; worker name, nationality, date of birth; proof of identity; qualification; job/occupation; commencement date; workplace; working hours; rest days; probation (if any); contract term; wage incl. benefits and allowances; annual leave entitlement; notice period; termination procedures; any other data the Ministry determines | "The employment contract should include the name and address of the employer, the name, nationality and date of birth of the worker" |
| CR 10(2) | The parties may add clauses to the approved forms if those clauses comply with the DL, the CR and the Legal Regulations. | none | "The worker and the employer may agree to introduce new clauses to the approved contract forms" |
| CR 10(3) | Changing from one work type to another requires: (a) both parties' approval, (b) payment of all entitlements under the original contract, (c) the Ministry procedure. | 3 conditions | "Payment of all the entitlements arising from the original contract." |
| CR 10(4) | Contract forms in the Ministry system. | Full-time; part-time; temporary work; flexible work; remote work; job sharing; any other form set by Ministerial resolution | "using the contract forms in the Ministry's system, namely: a. Full-time employment contract. b. Part-time employment contract." |
| DL 7(1) | Work patterns. | Full time (one employer, full daily hours); part time (one or more employers, specified hours or days); temporary (specific period or task); flexible (variable hours or days); others set by the CR | "Full time; which means working for one employer for full daily working hours throughout the working days." |
| CR 5(1) | Two additional work types. Job sharing is treated under the part-time rules. | Remote work (all or part outside the workplace, full- or part-time); job sharing (wage proportional to agreed tasks) | "They shall be treated according to the regulations of part-time work." |
| DL 66(1)–(2) | Arabic is the approved language of records and contracts. A second language the worker understands must sit beside the Arabic, and the Arabic prevails where they differ. Applies to contracts, instructions and circulars. | Arabic plus one language the worker understands; Arabic prevails | "In case of difference, the Arabic text shall prevail." |
| DL 68(1)–(3) | Undefined-term contracts made under Federal Law 8/1980 must be converted to fixed-term within one year of enforcement, and the Minister may extend that period. Gratuity for those contracts may be calculated under the old law. | 1 year from enforcement (2 Feb 2022), extendable by the Minister | "during one year from the date of its enforcement. The Minister may extend this period for other periods as required by the public interest." |
| DL 65(6) | Notice to end a pre-DL undefined-term contract, which needs a legitimate reason and written notice, depends on length of service. | Service < 5 yrs: ≥ 30 days. Service > 5 yrs: ≥ 60 days. Service > 10 yrs: ≥ 90 days. **AMBIGUOUS:** exactly 5 and exactly 10 years are not covered by the wording | "a period of not less than (30) thirty days if the service term is less than (5) five years, a period of not less than (60) sixty days" |
| DL 65(1), (3), (5) | The DL sets minimum rights. A clause that conflicts with it is void unless it is more beneficial to the worker. The employer may not revise a contract in force to apply the DL unless the change benefits the worker. | none | "Each provision contradicting the provisions hereof, even if it was existing prior to its enforcement, shall be deemed null and void, unless it is more beneficial to the worker." |

## 2. Work permits and worker classification

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 6(1) | No one may work, and no employer may recruit or employ, without a Ministry work permit. | none | "the employer may not recruit or employ any worker, except after obtaining a work permit from the Ministry" |
| CR 6(1) | **The 12 work-permit types:** (a) Work permit (recruiting a worker from outside the State); (b) Transfer work permit; (c) Work permit for residents sponsored by their families; (d) Temporary work permit; (e) Mission permit; (f) Part-time work permit; (g) Juvenile permit; (h) Student training and employment permit; (i) UAE / GCC national permit; (j) Golden visa holders permit; (k) National trainee permit; (l) Freelance permit. | Juvenile permit: from 15 years, not over 18. Student permit: student already in the State, from 15 years. Part-time: may work for more than one employer with a Ministry permit | "Juvenile permit: This type of permit is issued to a person who has reached 15 years of age but is not over 18 years" |
| CR 6(2) | The Minister may create new permit types by resolution. | none | "New work permits may be created by resolution of the Minister" |
| CR 7(1) | Conditions for issuing a permit: worker at least 18 (except juvenile and student permits); licensing requirements met; occupation consistent with the establishment's activity; valid licence; application filed by the authorised signatory. | Minimum age 18 | "Except for the juvenile permit and the student training or employment permit, the worker should be at least 18 years old." |
| CR 7(3)(d) | Cancelling a permit requires the establishment to acknowledge that it has paid all of the worker's entitlements. | none | "Acknowledgment by the establishment of granting the worker all of their entitlements." |
| CR 7(4)(c) | The Ministry may refuse, decline to renew or cancel permits if the WPS is not complied with. | none | "That the Wage Protection System or any other system adopted for the regulation of the national labour market is not complied with." |
| CR 3(1)–(2) | Workers are classified by criteria. **The text lists no skill levels and no level names**: the levels and their privileges are left to a separate Cabinet resolution. | Criteria: skill, educational qualifications, productivity, professional or salary levels, residency status | "classified into categories according to criteria that include skill, educational qualifications, productivity, professional or salary levels, according to residency status." |
| CR 2 | Establishments are classified by economic activity, headcount, diversity, compliance and Emiratisation/training support. Categories are set by Cabinet resolution and are not listed here. | none | "Establishments shall be classified according to criteria that include their economic activity, the number of workers employed" |

## 3. Probation

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 9(1) | Probation is at most 6 months from the start of work. To terminate during probation, the employer must give written notice at least 14 days ahead. | Max 6 months. Employer notice ≥ 14 days, written | "a probationary period not exceeding (6) six months from the date of commencement of work" / "in writing fourteen (14) days at least before the date specified" |
| DL 9(2) | Only one probation per worker per employer. Probation counts toward the service term. | Once per employer. Counts in service | "It is not permissible to appoint a worker under probationary period more than once at one employer" |
| DL 9(3) | A worker resigning during probation **to move to another UAE employer** gives at least one month's written notice. The new employer compensates the original employer for recruitment or contracting costs unless otherwise agreed. | Worker notice ≥ 1 month, written. Compensation = recruitment/contracting costs (no amount or cap stated) | "notify the original employer of the same in writing within not less than one month" / "the new employer shall compensate the original employer for the costs of recruitment" |
| DL 9(4) | A **foreign** worker resigning during probation **to leave the UAE** gives at least 14 days' written notice. If he returns and gets a new permit within 3 months of departure, the new employer pays the DL 9(3) compensation, unless the worker and the original employer agreed otherwise. | Worker notice ≥ 14 days, written. Return window 3 months | "notify the employer of the same in writing not less than fourteen (14) days" / "obtain a new work permit within (3) three months from the date of departure" |
| DL 9(5) | Either party that breaks the DL 9 notice rules pays the other the worker's wages for the notice period, or for the unserved remainder. | Compensation = wages for notice period, or the remainder of it | "compensation equal to the worker's wages for the notice period or the remaining period of the notice period." |
| DL 9(6) | A foreign worker who leaves the UAE without following DL 9 gets no work permit for one year. | 1-year permit ban | "he shall not be granted a work permit to work in the State for one year from the date of leaving the State." |
| DL 9(7) + CR 11 | Exemptions from the bans in DL 9(4) and 9(6). | Exempt: in-demand skill/professional/knowledge levels; family-sponsored residency; golden visa holders; categories set by Ministerial resolution | "The worker's residency visa is sponsored by his family." |
| DL 29(3) | The employer may grant annual leave during probation. If the worker fails probation, he is compensated for the remaining leave balance. | none | "the worker shall reserve his right to be compensated for the remainder of his annual leave balance in case he does not pass the probationary period." |
| DL 31(2) | No paid sick leave during probation. Unpaid sick leave may be granted on a medical report. | Paid sick leave during probation: 0 | "The worker shall not be entitled to a paid sick leave during the probationary period." |
| CR 12(5)(b) | The non-compete does not apply if the contract ends during probation. | none | "If the contract is terminated during the probationary period." |

## 4. Non-compete

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 10(1) | Allowed only where the job gives knowledge of clients or access to work secrets. It must be limited in time, place and type of work. | Max 2 years from contract expiry | "The non-competition period shall not be more than two years from the expiry date of the contract." |
| DL 10(2) | The clause is void if the employer terminates in violation of the DL. | none | "This requirement shall be nullified if the employer terminates the employment contract in violation of the provisions hereof." |
| DL 10(3) | The employer's claim is barred one year after it discovers the violation. | 1 year from discovery | "shall not be heard if one year has passed from the date of discovering the violation." |
| CR 12(1) | Required elements: geographical scope, duration of at most 2 years, and work whose nature could cause significant harm to the employer. | ≤ 2 years | "The duration of the clause, provided that it does not exceed two years from the contract expiry date." |
| CR 12(2) | Unsettled disputes go to the courts. The employer carries the burden of proving damage. | none | "the burden of proving the alleged damage shall lie with the employer." |
| CR 12(3)–(4) | The clause does not apply if termination is attributable to the employer or to its breach. The parties may agree in writing to waive it. | none | "shall not apply if the reason for terminating the contract is attributed to the employer" |
| CR 12(5) | Exemptions: (a) the worker or new employer pays compensation, with the previous employer's written consent; (b) termination during probation; (c) in-demand categories set by the Minister. | Buy-out ≤ 3 months' wage under the last contract | "compensation not exceeding three months of the worker's wage as agreed upon in the last contract" |

## 5. Employer obligations (records, documents, fees, certificates)

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 13(1) | Keep worker files and records as the Ministry prescribes, for at least 2 years after the end of service. | Retention ≥ 2 years after end of service | "the period of keeping the worker's file shall not be less than two years after the date of the worker's end of service." |
| DL 13(2) | Do not withhold the worker's official documents. Do not force the worker to leave the UAE at the end of employment. **The word "passport" does not appear in the text.** | none | "Not withholding the official documents of the worker or forcing him to leave the State at the end of the employment relationship." |
| DL 6(4) | The employer may not charge the worker recruitment or employment fees and costs, directly or indirectly. | none | "The employer is prohibited from charging the worker for the fees and costs of recruitment and employment or collecting them from him" |
| DL 13(3) + CR 14 | Work regulations: instructions, penalties, promotions, rewards and termination procedures. Mandatory for establishments with 50 or more workers. They must cover daily hours, weekly rest days, official holidays and injury/fire precautions, and be communicated in a language the worker understands. | Threshold: 50+ workers | "establishments that employ 50 or more workers shall establish the terms to govern employment practices" |
| DL 13(4) | Provide licensed accommodation, or pay an accommodation allowance in cash or as part of the wage. | none | "or paying to him an accommodation allowance in cash or including it in the wage." |
| DL 13(8)–(9) | Bear medical-care costs and the insurances, contributions and guarantees required by law. | none | "Bearing the costs of the worker's medical care in accordance with the legislation in force in the State." |
| DL 13(10) | Do not let the worker work for others except as the DL allows. | none | "Not allowing the worker to work for others, except in accordance with the provisions hereof." |
| DL 13(11) | On request at contract expiry, issue a free experience certificate stating start date, end date, total service, job title, last wage and termination reason. It must contain nothing harmful to the worker. | Fee: none | "a certificate of experience, without fees, indicating the date of his commencement of work, the date of its expiry, his entire service term" |
| DL 13(12) | Pay repatriation to the place of recruitment or an agreed place. Not owed if the worker has joined another employer or the termination is attributed to him, in which case he bears the cost. | none | "Bearing the repatriation expenses of the worker to his place of recruitment or any other place that both parties had agreed upon" |
| DL 16(10) | The worker must vacate employer accommodation within 30 days of end of service, unless the employer approves a longer stay at the worker's cost. | 30 days | "Evacuating the accommodation provided by the employer, within a period not exceeding (30) thirty days from the date of end of his service." |
| CR 4(3)(a) | Keep a special juvenile register: name, age, guardian's name and contact, residence of juvenile and custodian, employment date, and work assigned. | none | "Keeping a special record of juveniles, including the name and age of the juvenile, the full name and contact details of their guardian" |
| CR 24(3) | The disciplinary report is deposited in the worker's private file (see §9). | none | "recording the foregoing in a report to be deposited in their private file" |
| DL 14 | Forced labour, sexual harassment, bullying and verbal, physical or psychological violence are prohibited. | none | "Sexual harassment, bullying or any verbal, physical or psychological violence committed against the worker … are prohibited." |

## 6. Working hours, overtime, weekend, public holidays

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 17(1) | Maximum normal hours. | 8 h/day or 48 h/week | "The maximum normal working hours for workers shall be (8) eight hours per day or (48) forty-eight hours per week." |
| CR 15(2) | Ramadan reduction. | −2 h/day ("regular working hours"). **AMBIGUOUS:** the text does not say whether this applies to all workers or only to Muslims | "The regular working hours shall be reduced by two hours during the holy month of Ramadan." |
| DL 18 | At most 5 consecutive hours without a break. Breaks total at least 1 hour and are not counted as working hours. Shift and field jobs may be arranged differently. | ≤ 5 h consecutive. Break ≥ 1 h total, unpaid time | "The worker may not work for more than (5) five consecutive hours without a break or breaks of not less than an hour in total" |
| DL 17(3) + CR 15(1) | Commute time is not working time, except for: weather delays per NCM warnings; delays in employer transport after an accident or breakdown; or an express contract term. | 3 exceptions | "shall be counted within the working hours in the following cases" |
| DL 19(1) + CR 15(3) | Overtime is at most 2 h/day, unless needed to prevent or mitigate a serious loss or accident. Total hours are capped over 3 weeks. | OT ≤ 2 h/day. Total ≤ 144 h per 3 weeks | "the total working hours shall not exceed (144) one hundred and forty four hours every (3) three weeks." |
| DL 19(2) | Overtime pay = the normal-hours wage, calculated on basic wage, plus at least 25%. | +25% minimum, on basic wage | "calculated according to the basic wage plus an increase of not less than (25 %) twenty five percent of that wage." |
| DL 19(3) | Overtime between 22:00 and 04:00 is paid at least +50%. Shift workers are excluded from this clause. | +50% minimum, on basic wage. Window 10 pm–4 am. Shift workers excluded | "between 10 pm and 4 am … plus an increase of not less than (50 %) fifty percent of that wage." |
| DL 19(4) | Work on the contractual weekend earns a substitute day off, or that day's wage plus at least 50% of the basic wage. | Day off, or +50% of basic | "plus an increase of not less than (50 %) fifty percent of the basic wage for that day." |
| DL 19(5) | No more than two consecutive weekend days may be worked, except by day workers. | Max 2 consecutive weekend days | "A worker shall not be instructed to work for more than two consecutive weekend days, except for day workers." |
| DL 21 | Paid weekend of at least one day. The Cabinet may increase it. | ≥ 1 paid day/week | "The worker shall be granted a paid weekend of not less than one day" |
| DL 28(1) | Public holidays are paid days off. The list is set by Cabinet resolution and **is not in this text**. | Full pay | "The worker shall be entitled to official days off with full pay on public holidays, which are defined by a resolution of the Cabinet." |
| DL 28(2) | Work on a public holiday earns a substitute day off for each day, or the day's wage plus at least 50% of the basic wage. | Day off, or +50% of basic | "compensate him with another day off for each day, on which he works during the holiday" |
| DL 20 + CR 15(4) | Exempt from the maximum-hours rules: board chairs and members; supervisors holding employer authority; ship crews and seafarers; continuous technical shift work; preparatory or supplementary work outside normal hours. | Continuous shifts: average ≤ 56 h/week | "subject to the condition that the average working hours do not exceed (56) hours per week." |
| DL 17(5) | Non-full-time workers may not be asked to exceed their contracted hours without written consent. | none | "except with the written consent of the worker." |
| DL 5(2)(c)–(f) | Juveniles (15–17) work at most 6 h/day with breaks of at least 1 h total and no more than 4 consecutive hours. They may not work 19:00–07:00, overtime, weekends or official holidays. They also need written guardian consent and a medical fitness certificate (DL 5(2)(a)–(b)). | 6 h/day. Break ≥ 1 h. ≤ 4 h consecutive. Banned 7 pm–7 am | "The juvenile shall not work between 7 pm and 7 am." |

## 7. Wages: payment, currency, WPS, deductions

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 22(1) | The wage amount or type must be in the contract. If it is not, the court sets it. | none | "The amount or type of wage shall be specified in the employment contract" |
| DL 22(2) + CR 16(1)(a) | Pay on the due dates agreed in the contract, per Ministry rules. **No specific day or grace period is stated.** | Due date = per contract | "The wages shall be paid on their due dates as agreed upon in the contract" |
| CR 16(1)(b) | Pay through WPS or another Ministry-approved system. Applies to all Ministry-registered establishments. | WPS mandatory | "shall pay the wages of their workers on their due date through the Wages Protection System or through any other system approved by the Ministry." |
| CR 16(1)(c) | Provide proof of wage payment on request. | none | "All establishments shall submit whatever is required of them to prove payment of the wages" |
| DL 22(3) | Currency is AED. Another currency is allowed if agreed in the contract. | AED default | "The salaries shall be paid in UAE Dirham and may be paid in another currency if it is agreed upon" |
| DL 23 | Piecework daily wage = average received over actual working days in the previous 6 months. | 6-month average | "according to the average amount the worker received for the actual working days during the (6) six months preceding" |
| DL 24 | Moving a monthly-paid worker to a daily, weekly, piecework or hourly basis requires written consent. Acquired rights are preserved. | none | "if the worker agrees on the same in writing" |
| DL 25(1)(a) | Loan repayment needs written consent and no interest, within the article's monthly deduction limit. **AMBIGUOUS:** no loan-specific percentage is given, so the only applicable cap is the 50% overall cap in DL 25(2). | Interest: 0 | "after obtaining the worker's written consent and without any interest." |
| DL 25(1)(b) | Recovery of overpayments. | ≤ 20% of wage | "provided that the amount deducted does not exceed (20%) twenty percent of the wage." |
| DL 25(1)(c)–(e) | Pension and insurance contributions under law. Savings Fund contributions or loans approved by the Ministry. Ministry-approved social-project instalments with written consent. | No % stated | "The worker's contributions to the Savings Fund at the establishment or the loans payable to the Fund approved by the Ministry." |
| DL 25(1)(f) | Disciplinary fines under the Ministry-approved penalty regulation. | ≤ 5% of wage | "provided that they shall not exceed (5%) five percent of the wage." |
| DL 25(1)(g) | Court-judgment debts. Alimony may exceed this cap. Several debts are paid by order of privilege. | ≤ 1/4 of wage (except alimony) | "without exceeding a quarter of the wage payable to the worker, except for the awarded alimony debt" |
| DL 25(1)(h) | Damage to employer property through the worker's fault. A higher deduction needs court approval. | ≤ 5 days' wage per month | "provided that the deducted amounts do not exceed the wage of (5) five days per month." |
| DL 25(2) | Overall cap on all deductions and withholdings combined. | ≤ 50% of wage | "the percentage of deduction and/or withholding may not exceed (50%) fifty percent of the wage." |
| DL 26 + CR 17 | If the employer does not let the worker work, it still pays the agreed wage, including when the cause is beyond its control. The worker may complain. The Ministry may then cancel the permit and allow a transfer if the employer does not respond within its grace period. | Grace period: set by the Ministry, no number given | "the employer shall inform the worker thereof along with guaranteeing the payment of their wages." |
| DL 27 | Minimum wage may be set by Cabinet resolution. **No figure is in this text.** | none | "issue a resolution to determine the minimum wage for workers or any category thereof." |
| DL 54(5) **AMENDED** (Federal Decree-Law No. (9) of 2024) + CR 31(4) | During a dispute, the Ministry may require the employer to keep paying wages. | ≤ 2 months' wages | "continue to pay the worker's wages for a maximum period of two (2) months" |

## 8. Leaves

### 8a. Annual leave

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 29(1)(a) | Full-wage annual leave for each year of service. | ≥ 30 days/year. **AMBIGUOUS:** calendar or working days is not stated | "Thirty days for each year of extended service." |
| DL 29(1)(b) | First-year accrual. **Nothing is stated for service of 6 months or less.** Whether service of exactly 6 months qualifies is also ambiguous. | 2 days/month when service > 6 months and < 1 year | "Two days for each month if his service term is more than six months and less than a year." |
| DL 29(1)(c) | Pro-rata leave for part of the final year if service ends before the balance is used. | Pro rata | "A leave for parts of the last year he spent at work if his service is ended before using his annual leave balance." |
| DL 29(4) | Leave is taken in the year it is earned. The employer may set dates for work needs, with at least one month's notice. | Notice ≥ 1 month | "The employer shall notify the worker of the specified date for his leave within a sufficient time of not less than a month." |
| DL 29(5) + CR 19(1) | Carry-forward needs employer approval. Alternatively, agree a cash allowance at the wage current when the leave fell due. | Carry-forward ≤ 1/2 of annual leave. Cash at "the wage" then received (not stated as basic) | "The worker may carry forward not more than half of the annual leave to the following year" |
| DL 29(6) | Wage is paid during leave. | Full wage | "The worker shall be entitled to the wage for the period of his annual leave." |
| DL 29(7) | Legal or agreed holidays falling inside annual leave count as part of the leave, unless the contract or regulations are more favourable. | none | "The holidays prescribed by law or by agreement are included in the calculation of the annual leave period if they fall within the annual leave" |
| DL 29(8) | The employer may not stop the worker using leave accrued over more than two years, unless the worker wants to carry it forward or be paid for it. **AMBIGUOUS:** the English does not clearly set a hard 2-year expiry or forfeiture. | 2 years | "The employer may not prevent the worker from benefiting from his annual leave accrued for more than two years" |
| DL 29(9) + CR 19(2) | Leaving before using accrued leave: cash in lieu for all accrued days whatever the balance, plus pro rata for the partial year. Paid on **basic wage**. | Basis: basic wage | "it shall be calculated according to the basic wage." / "a cash allowance for the balance of their legally due annual leave, according to the basic wage." |
| DL 29(2) + CR 18 | Part-time leave formula: contracted part-time hours per year ÷ full-time hours per year × 100 = %, applied to the legal leave. Daily hours are counted at most 8. A fraction of a day rounds up to a full day. | Minimum 5 working days/year. Max 8 h/day counted. Fractions round up | "with a minimum of five working days per year for annual leave, and a fraction of a day considered as a full day" |

### 8b. Maternity, sick and other leaves

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 30(1) | Maternity leave is 60 days. **No amendment marker on this article in the booklet.** | 60 days = 45 full wage + 15 half wage | "a maternity leave of (60) sixty days … The first (45) forty-five days with full wage. … The following (15) fifteen days with half wage." |
| DL 30(2) | After maternity leave, up to 45 days unpaid absence (continuous or intermittent) for pregnancy- or birth-related sickness of mother or child, with a medical certificate. **Not counted** in service for gratuity. | ≤ 45 days unpaid. Excluded from service | "be absent from work without a wage for a period not exceeding continuous or intermittent (45) forty-five days" |
| DL 30(3) | Maternity leave applies if delivery is at least 6 months into pregnancy, including stillbirth or a child born alive who then dies. | ≥ 6 months' pregnancy | "if the delivery took place (6) six months or more after pregnancy" |
| DL 30(4) | Sick child or child of determination needing a constant companion (medical report): extra leave after maternity leave. | 30 days full pay + optional 30 days unpaid | "a leave of thirty (30) days with full pay starting after the end of the maternity leave" |
| DL 30(5) | Earliest start: the last day of the month before the expected birth month, on request, with a medical certificate. | none | "starting from the last day of the month preceding immediately the month, in which she is expected to give birth" |
| DL 30(7)–(8) | Working for another employer during the leave allows the employer to withhold or recover leave pay. No termination or notice because of pregnancy or leave. | none | "It is not permissible to terminate the service of the female worker or notify her of the same because of the pregnancy" |
| DL 30(9) | Nursing breaks. | Up to 6 months from delivery. 1–2 breaks/day totalling ≤ 1 h | "one or two breaks per day to breastfeed her child, provided that the two breaks do not exceed an hour." |
| DL 31(1) | Notify the employer of sickness and submit a medical report. | Within ≤ 3 working days | "within a period not exceeding (3) three working days" |
| DL 31(3) | Sick leave after probation. | ≤ 90 days/year (continuous or intermittent) = 15 full pay + 30 half pay + remainder unpaid | "The first (15) fifteen days with full pay. b. The following (30) thirty days with half pay. c. The following period unpaid." |
| DL 31(4) + CR 20 | No sick pay where the sickness results from misconduct (alcohol, drugs) or from breach of informed safety instructions. A report from the concerned authorities is required for the misconduct case. | none | "If the disease resulted from the worker's misconduct, such as their consumption of alcohol or drugs." |
| DL 31(5) | The employer may terminate after sick leave is exhausted if the worker cannot return, paying all entitlements. | none | "The employer may terminate the worker's service after finishing his sick leave" |
| DL 32(1)(a) + CR 21(3) | Paid bereavement leave from the date of death. Proof of death is submitted on return. | Spouse: 5 days. Parent, child, sibling, grandchild, grandparent: 3 days | "A bereavement leave of (5) five days, in case of death of the husband or wife and (3) three days in case of death of the mother, father" |
| DL 32(1)(b) + CR 21(4) | Paid parental leave for father or mother, continuous or intermittent, with proof of birth. | 5 working days, within 6 months of birth | "A parental leave for a period of (5) five working days … within (6) six months from the date of the child birth." |
| DL 32(2) + CR 21(1) | Paid study leave for exams at an accredited UAE institution. The employer may ask for exam dates. Note DL 32(2) says the worker "may be granted" it. | 10 working days/year. Service ≥ 2 years | "a study leave for a period of (10) ten working days per year … provided that the service term at the employer is not less than two years." |
| DL 32(3) + CR 21(2) | UAE nationals: sabbatical paid leave for national (and reserve) service, per other legislation. | No duration stated | "The national worker shall be entitled to a sabbatical paid leave to perform the national service" |
| CR 21(5) | Bereavement, parental, annual and unpaid leave may be combined. | none | "The bereavement leave, parental leave, annual leave and unpaid leave may be combined." |
| DL 33 | Unpaid leave with the employer's approval. **Excluded** from the service term. | No max stated | "The leave mentioned in this Article shall not be included in the worker's service term at the employer" |
| DL 34 | No wage for the absence if the worker does not return straight after leave without a legitimate reason. | none | "shall not be entitled to his wage for the absence period following the leave end." |
| DL 35 | Notice of termination given during leave starts only on the day after the scheduled return, unless agreed otherwise. | none | "shall not begin, except from the day following the day scheduled for the worker's return from the leave" |

## 9. Disciplinary sanctions

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 39(1) | The only permitted penalties: (a) written notice; (b) written warning; (c) wage deduction; (d) suspension without pay; (e) loss of periodic bonus; (f) loss of promotion; (g) termination with gratuity preserved. | (c) see the ambiguity below. (d) ≤ 14 days unpaid. (e) ≤ 1 year. (f) ≤ 2 years | "Suspension from work for a period not exceeding (14) fourteen days and non-payment of wage for the suspension days." |
| DL 39(1)(c) | Wage-deduction penalty. **AMBIGUOUS, and it contradicts DL 25(1)(f):** the English says "not less than" 5 days per month, while DL 25(1)(f) caps fines at 5% of the wage. Check the Arabic text before encoding this. | "not less than (5) five days per month" (verbatim) | "Deduction of not less than (5) five days per month from the wage;" |
| DL 40(1) | Suspension pending investigation, on half wage. If the case is shelved, the worker is cleared, or only a warning results, the withheld half is repaid. | ≤ 30 days. 50% wage withheld | "suspend the worker temporarily from work for a period not exceeding (30) thirty days … along with suspending half the wage" |
| DL 40(2) | Suspension when accused of a crime of assault, money, honour or trust, until final judgment, with wage suspended. Full back-pay if not tried, acquitted, or shelved for lack of evidence. | Wage 100% suspended | "His wage shall be suspended for the suspension period." |
| DL 41 | No penalty for off-workplace conduct unless work-related. Only one penalty per violation. | 1 penalty per violation | "It is not permissible to impose more than one disciplinary sanction for a single violation" |
| CR 24(1) | Severity criteria: confidentiality breach, health and safety impact, financial impact, reputational impact, abuse of power, recurrence, penal or moral element. | 7 criteria | "taking into consideration the appropriate penalty depending on the gravity and seriousness of the committed violation" |
| CR 24(2) | The employer must publish a list of penalties mapped to the DL 39 sanctions. | none | "The employer shall establish a list of penalties clarifying each of the disciplinary sanctions set out in Article (39)" |
| CR 24(3) | Due process: written charges, hearing, investigation of the defence, and a report placed in the file. The worker is told in writing the penalty, amount, grounds and the consequence of recurrence. | Written at each step | "except after informing them in writing of the charges against them, hearing their statements, investigating his defence" |
| CR 24(4) | Time limits. | Charge within 30 days of detection. Penalty within 60 days of the investigation's conclusion | "detected more than (30) thirty days ago, and no disciplinary sanction may be imposed more than (60) days after" |
| CR 24(5)–(6) | Internal grievance right. Employers with 50 or more workers must publish a complaints and grievance system with written answers "within a specific period" (no number given). | Threshold 50+ workers | "every employer who employs (50) or more workers shall put in a visible place … a system for complaints and grievance claims" |
| CR 29(1)(c), (2) | Fines may also be deducted from gratuity (see §12). | — | — |

## 10. Termination

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 42 | Termination cases: (1) written mutual agreement; (2) expiry unless extended or renewed; (3) either party's wish, with notice observed; (4) employer's death if the contract relates to his person; (5) worker's death or full permanent inability (medical certificate); (6) final judgment imposing a freedom-restricting penalty; (7) permanent closure; (8) bankruptcy, insolvency or economic or exceptional reasons; (9) worker fails the permit-renewal conditions for reasons beyond the employer's control. | (6) penalty ≥ 3 months | "A final judgment issued against the worker by a freedom-restricting penalty for a period of not less than (3) three months." |
| CR 25 | Bankruptcy or insolvency termination needs a court ruling, or an authority decision that the employer cannot continue for exceptional economic reasons. | none | "Issuance of a court ruling adjudicating the employer's bankruptcy or insolvency" |
| DL 43(1) | Either party may terminate for a legitimate reason with written notice. | Notice min 30, max 90 days | "provided that such period is not less than (30) thirty days and not more than (90) ninety days." |
| DL 43(2) | The contract stays in force during notice. Full wage is paid at the **last wage**. The worker works the notice if the employer asks. Notice may be waived or shortened by agreement, with the worker's rights preserved. Notice is the same for both parties unless it favours the worker. | Same length both ways (unless better for the worker) | "provided that the notice period is the same for both parties unless it serves the interests of the worker." |
| DL 43(3)–(4) | Payment in lieu (notice period allowance) is due even if no damage was caused. It is calculated on the **last wage** (monthly, weekly, daily, hourly), or on the average daily wage for piecework. | Full notice, or the unserved remainder | "the compensation shall be equal to the worker's wage for the full notice period or the remaining part thereof." |
| DL 43(5) | During notice given by the employer, the worker may take one unpaid day per week to job-hunt, notifying the employer 3 days ahead. | 1 day/week unpaid. Notify ≥ 3 days | "one working day without pay per week, in order to search for another job" |
| DL 44 | Dismissal without notice needs a written investigation and a written, justified decision handed to the worker. Ten grounds: forgery or impersonation; gross loss or deliberate damage (Ministry informed within 7 working days); posted safety-rule breach; continued breach of basic duties after investigation and 2 warnings; disclosure of a secret causing loss; intoxication or immorality; assault; unjustified absence; abuse of position; joining another establishment unlawfully. | Absence ground: > 20 intermittent days/year or > 7 consecutive days. Ministry notice 7 working days. Warnings: 2 | "more than (20) twenty intermittent days during one year or more than (7) seven consecutive days." |
| DL 45 | The worker may quit without notice, keeping end-of-service rights, if: (1) employer breach, with the Ministry notified 14 working days ahead and no remedy after Ministry notice; (2) assault, violence or harassment, reported within 5 working days; (3) grave danger the employer knows of; (4) fundamentally different work without written consent (except DL 12 necessity). | 14 working days. 5 working days | "provided that the worker notifies the Ministry fourteen (14) working days before the date of quitting work" |
| CR 26 | Grave-danger list for DL 45(3): ignition source; live electrical wires; hazardous chemicals; unusual temperatures causing burns; noise causing permanent hearing damage; radiation; biological hazards. | 7 items | "Presence of a possible source of ignition." |
| DL 46 | No termination for medical unfitness before accrued leaves are used. Contrary agreements are void. | none | "The employer may not terminate the worker's service due to his lack of health fitness before using the legally accrued leaves." |
| DL 47 | Termination is unlawful if it is because of a serious complaint to the Ministry or a proven lawsuit. The court sets fair compensation, in addition to notice allowance and gratuity. | Cap: 3 months' wage at **last wage** | "the amount of compensation does not exceed the worker's wage for a period of (3) three months, calculated according to the last wage" |
| DL 30(8) | No termination or notice because of pregnancy, maternity leave or DL 30 absence. | none | (see §8b) |
| DL 9(5) | Probation notice breach: see §3. | — | — |
| DL 12 + CR 13 | Temporary assignment to fundamentally different work: allowed only for necessity, accident prevention or damage repair, up to 90 days a year. Otherwise written consent is needed. | ≤ 90 days/year | "The maximum limit for assigning the worker to such work shall be of (90) ninety days per year." |
| DL 49 + CR 27 | Transfer to a new employer is allowed if the contract ends unrenewed, is terminated under DL 42 or 45, or the employer terminates without cause attributable to the worker. | none | "If the employer terminates the contract without a reason attributed to the worker." |

## 11. Unlawful absence / absconding

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 50(1) | A foreign worker who leaves work illegitimately before the contract ends gets no new permit for 1 year from the absence date. Other employers who know may not employ him. | 1-year ban | "for a period of one year from the date of the absence from work." |
| DL 50(3) + CR 28(1) | The employer reports to the Ministry once absence exceeds 7 consecutive days, location unknown and the worker unreachable, using the Ministry's absence form. | Trigger: > 7 consecutive days | "The absence from work shall have exceeded 7 consecutive days, without the employer's knowledge of the worker's location" |
| CR 28(2) | Exceptions to the 1-year ban: family-sponsored residency; new permit at the same establishment; in-demand skills; golden visa; categories set by the Minister. | 5 exceptions | "Workers who apply for a new work permit at the same establishment." |
| DL 44(8) | Related dismissal ground (§10). | > 20 intermittent / > 7 consecutive days | — |

## 12. End-of-service gratuity

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 51(1) | UAE nationals: governed by pensions and social-security legislation, not by this formula. | — | "The national worker shall be entitled to end of service benefits … in accordance with the legislation regulating the pensions and social securities" |
| DL 51(2) | Full-time **foreign** worker with at least 1 year of continuous service. Calculated on **basic wage**. | 21 days' wage per year for years 1–5. 30 days' wage per year after that | "A wage of (21) twenty-one days for each year of the first five years of service; b. A wage of (30) thirty days for each year exceeding such period." |
| DL 51(3) | Part years are paid pro rata, provided 1 year of continuous service is complete. | < 1 year = nothing | "a benefit for parts of the year in proportion to the period spent at work, provided that he completed one year of continuous service." |
| DL 51(4) | Unpaid days of absence are excluded from service. (Also excluded: DL 30(2) 45-day post-maternity absence and DL 33 unpaid leave.) | Exclude unpaid days | "The unpaid days of absence from work shall not be included in the calculation of the service term." |
| DL 51(5) | Basis: **last basic wage** for monthly, weekly and daily pay. Average daily wage (DL 23) for piecework. | Last basic wage | "calculated according to the last basic wage the worker was entitled to" |
| DL 51(6) | Cap. | Total ≤ 2 years' wage | "the end of service benefits for the foreign worker in its entirety does not exceed two years' wage." |
| DL 67 | Day/month/year conventions used in the calculation. | Year = 365 days. Month = 30 days. **AMBIGUOUS:** the text does not give a "daily basic wage = monthly ÷ 30" formula explicitly. It only defines the month as 30 days | (see §14) |
| DL 51(7) + CR 29(1) | Deductions allowed from gratuity: loan repayments and overpayments; pension and insurance contributions; disciplinary fines under the approved regulation; court-ordered debts; damage caused by fault or breach of instructions. | 5 categories | "any amounts that are due legally or by judicial ruling" |
| CR 29(2) | Fines and damage deductions need the DL/CR procedure, and no more than 3 months may have passed since the amount fell due, unless agreed otherwise. | ≤ 3 months since due | "not more than (3) three months shall have lapsed from the due date of such amounts unless otherwise agreed." |
| DL 52 + CR 30(1) | Part-time and job-sharing gratuity: (contract hours per year ÷ full-time hours per year × 100) % × the full-time gratuity. **Flexible work is not mentioned in CR 30.** | Pro-rata % | "this percentage should be multiplied by the value of the end of service benefit due for the full-time employment contract." |
| CR 30(2) | Temporary employment under 1 year: no gratuity. | < 1 year = 0 | "The end of service benefit shall not apply in the case of temporary employment with a duration of less than one year." |
| DL 53 | All wages and entitlements are paid within 14 days of the contract's end date. | 14 days | "within (14) fourteen days from the end date of the contract term, his wages and all his other entitlements" |
| DL 39(1)(g) | Termination as a disciplinary penalty keeps gratuity. | — | "Termination of service while preserving the worker's right of end of service benefits." |
| DL 51(8) | **Alternative scheme:** the Cabinet may approve alternative schemes, with terms set by that resolution. **No specific scheme, fund or contribution rate is named in this text.** | none | "the Cabinet may … approve other alternative schemes for the end of service benefits scheme" |
| DL 25(1)(d) | Related: a Savings Fund at the establishment, Ministry-approved, may receive wage deductions. | No rate | "The worker's contributions to the Savings Fund at the establishment" |
| DL 65(7) | Amounts owed to the worker or family rank ahead of all of the employer's funds, after public-treasury dues and legal alimony. | Priority | "shall have a concession over all the funds of the employer" |
| DL 68(3) | Legacy undefined-term contracts may be calculated under Federal Law 8/1980. | — | (see §1) |

## 13. Death of the worker

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 15(1) | Wages, dues and gratuity are handed to the worker's family (spouse, sons, daughters, per DL 1). | ≤ 10 days from death, or from when the employer learned of it | "within a period not exceeding (10) ten days from the date of death or from the date on which the employer became aware" |
| DL 15(2) | The worker may nominate in writing a family member to receive his rights. | Store the nominee | "the worker may specify in writing the concerned person from his family to receive his rights in case of his death." |
| DL 15(3) | The employer bears preparation and transport of the body home if the family asks. | Employer cost | "The employer shall bear all the costs of preparing and transporting the corpse of the deceased worker" |
| DL 15(4) | The Ministry may set a mechanism to hold entitlements that cannot be handed over. | — | — |
| DL 42(5) | Death ends the contract. | — | "The worker's death or full permanent inability to work" |
| DL 37(3) + CR 23(4) | If death results from a work injury or occupational disease, the family receives compensation in addition to gratuity and other dues. It is distributed per the legislation, or as the worker determined before death. | 24 months' **basic wage**, min AED 18,000, max AED 200,000 | "equal to the basic wage of the worker for (24) twenty-four months, provided that the compensation amount is not less than (18,000)" |
| DL 37(2)(b) | Related (injury, not death): wage during work-injury treatment. | Full wage for treatment or 6 months, whichever is less. Then half wage for another 6 months, or until recovery, disability or death | "the worker shall obtain half wage for another (6) six months" |

## 14. Calculation of periods and dates

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 67 | All periods and dates use the Gregorian calendar. | Year = 365 days. Month = 30 days | "The Gregorian year in applying the provisions hereof shall include (365) three hundred and sixty-five days, while the month represents (30) thirty days." |
| (various) | Working days vs calendar days. The text uses "working days" explicitly for: sick notification (3), parental leave (5), study leave (10), DL 44(2) Ministry notice (7), DL 45 notices (14 and 5), part-time minimum leave (5). Elsewhere it says "days" without qualification, e.g. annual leave 30, maternity 60, notice 30–90, bereavement 5/3, payment 14. **Not defined further in this text.** | — | — |

## 15. Penalties (DL 58–64)

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 58 | These penalties do not prejudice a severer penalty under another law. | — | "shall not prejudice any severer penalty stated in any other law." |
| DL 59 | False documents to recruit a foreign worker; obstructing an inspector; an official disclosing work secrets. | AED 20,000 – 100,000 | "a fine of not less than (20,000) twenty thousand UAE Dirham and not more than (100,000) one hundred thousand UAE Dirham" |
| DL 60(1) **AMENDED** (Federal Decree-Law No. (9) of 2024) | (a) employing without a work permit; (b) recruiting and then not providing work; (c) misusing permits; (d) closing or ceasing operations without settling employees' dues; (e) employing a juvenile unlawfully; (f) a guardian agreeing to unlawful juvenile employment. | AED 100,000 – 1,000,000 | "A fine of at least (100,000) one hundred thousand UAE Dirham and up to (1,000,000) one million UAE Dirham" |
| DL 60(2)–(4) **AMENDED** (Federal Decree-Law No. (9) of 2024) | Fictitious employees (e.g. to game Emiratisation incentives). The fine is multiplied by the number of fictitious employees, and incentives must be repaid. Only the Minister may prosecute. Settlement is available. | AED 100,000 – 1,000,000 per employee. Settlement ≥ 50% of the minimum fine | "The penalty stipulated in this Clause shall be multiplied by the number of employees fictitiously appointed." |
| DL 61 | Misusing electronic access to Ministry systems. | Imprisonment ≥ 1 year and/or AED 200,000 – 1,000,000 | "imprisonment for a period of not less than one year and a fine of not less than (200,000) two hundred thousand UAE Dirham" |
| DL 62 | Employer fines multiply with the number of workers affected. | Max AED 10,000,000 | "with a maximum of (10,000,000) ten million UAE Dirham." |
| DL 63 | Catch-all for any other violation of the DL, CR or resolutions. **This is the only bracket that would cover non-payment of wages via WPS; no WPS-specific fine is stated.** | AED 5,000 – 1,000,000 | "shall be punished with a fine of not less than (5,000) five thousand UAE Dirham and not more than (1,000,000) one million UAE Dirham." |
| DL 64 | Repeat offence within 1 year of punishment for a similar violation: imprisonment and/or double the fine. | 1-year window. 2× fine | "imprisonment, along with doubling the fine stipulated herein or one of these penalties." |
| CR 34 | The Ministry may impose administrative penalties under Article 3 of Federal Law No. (14) of 2016. **That list is not reproduced in this text.** | — | "as stated in Article (3) of Federal Law No. (14) of 2016" |
| CR 7(4)(c) | Administrative consequence of WPS non-compliance: permits may be refused, not renewed or cancelled (§2). | — | — |

## Related limits an HR system may need

| Source | Rule | Parameters | Quote |
|---|---|---|---|
| DL 54(9) **AMENDED** (Federal Decree-Law No. (9) of 2024) | Limitation period for labour claims. | 2 years from end of the employment relationship | "shall not be considered after two years of the termination of the employment relationship." |
| DL 54(2)–(3) **AMENDED** (Federal Decree-Law No. (9) of 2024) | The Ministry may decide claims itself. Appeal to the Court of Appeal within 15 working days. | Claims ≤ AED 50,000 (or a breached amicable settlement of any value). Appeal 15 working days | "if the value of the claim is not more than (50,000) fifty thousand dirhams" |
| CR 31(2) | Unresolved complaint is referred to court. **Possible inconsistency:** amended DL 54(4) instead refers to a time limit "prescribed in the implementing regulation", and CR 31 carries no amendment marker. | 14 days from complaint | "the Ministry shall refer the dispute to the competent court within (14) fourteen days from the date of submission of the complaint" |
| DL 55 | Court-fee exemption for workers' claims. | ≤ AED 100,000 | "whose amounts do not exceed (100,000) one hundred thousand UAE Dirham." |
| CR 35 | Grievance against a Ministry decision. | Within 30 days of becoming aware of it | "within (30) thirty days from the date of becoming aware of the resolution." |
| DL 70(7) | The Cabinet may change any period, percentage or value in the DL. Treat every number here as configurable. | — | "Changing the periods, percentages, or values mentioned herein" |
| CR 36 | In Cabinet-declared emergencies: remote work, paid or unpaid leave, or wage reduction. | — | "Reducing the worker's wage." |

---

## Amendments noticed

The booklet marks only three articles as amended, all in the Decree-Law:

1. **DL 8(3)**: footnote "In accordance with Federal Decree-Law No. (14) of 2022 regarding amending some provisions of Federal Decree Law No. (33) of 2021". The current text has fixed-term contracts with renewal by agreement and **no stated maximum term**.
2. **DL 54** (Individual Labour Disputes, all 9 clauses): "amended in accordance with Federal Decree-Law No. (9) of 2024". It covers the Ministry deciding claims up to AED 50,000, the appeal deadlines, up to 2 months' continued wages, and the 2-year limitation.
3. **DL 60** (Penalties): "amended in accordance with the Federal Decree-Law No. (9) of 2024". It sets AED 100k–1M fines, the fictitious-employee offence and the ≥ 50% settlement.

No article of Cabinet Resolution 1/2022 carries an amendment marker. The booklet does not say whether the CR text shown is original or consolidated. **No amendment marker appears on DL 30 (maternity), DL 31 (sick), DL 32 (other leaves) or DL 51 (gratuity)**, so the figures above are what this booklet states as current. Verify against any later decree-law before go-live.

## Not found in this text, and ambiguities to resolve

**Skipped or absent:**
- **Topic 2 (skill levels):** CR 3 gives only classification criteria. No skill levels, level numbers or names, and no level-specific rules. Contract forms "according to the approved skill levels" (DL 8(6)) are not listed beyond the work-type forms in CR 10(4).
- **Topic 1 (fixed-term maximum):** no maximum duration or renewal count in amended DL 8(3).
- **Topic 7:** no specific pay day, grace period or "late wage" threshold. No WPS-specific fine (only DL 63's general AED 5k–1M and CR 7(4)(c)). No minimum-wage figure. No loan-specific deduction percentage.
- **Topic 5:** the word "passport" does not appear ("official documents" only). No retention period for payroll or other records beyond the ≥ 2-year worker file in DL 13(1).
- **Topic 6:** no list of public holidays (left to Cabinet resolution). No Ramadan rule restricted to Muslims.
- **Topic 8:** no annual-leave entitlement for service of 6 months or less. No maximum for unpaid leave. No duration for national-service sabbatical. No working-vs-calendar-day definition for the 30-day annual leave.
- **Topic 12:** no named alternative or savings scheme (DL 51(8) only empowers the Cabinet). No explicit daily-wage divisor (only DL 67's 30-day month). No gratuity rule for flexible work (CR 30 covers part-time and job-sharing only). No forfeiture of gratuity on resignation: the text has no resignation reduction.
- **Topic 15:** CR 34 refers to Federal Law 14/2016 Art. 3 administrative penalties, which are not reproduced here.

**Ambiguities to check against the Arabic text (DL 66 says Arabic prevails):**
- **DL 39(1)(c)** "Deduction of not less than (5) five days per month" conflicts with the DL 25(1)(f) cap of 5% of wage on fines. This is the most important one to resolve before encoding penalty deductions.
- **DL 29(8):** the leave-older-than-2-years wording does not clearly create forfeiture.
- **DL 65(6):** exactly 5 or exactly 10 years of service is not covered by "less than 5 / more than 5 / more than 10".
- **DL 29(1)(b):** "more than six months" leaves exactly-6-months unclear.
- **CR 19(1) vs DL 29(9) / CR 19(2):** encashment while employed is at "the wage" received at the time of entitlement, while encashment at end of service is at **basic** wage. Two different bases, as written.
- **DL 43(2)/(4) and DL 47(2):** notice pay and unlawful-termination compensation use the "last wage" (full wage), not basic. Gratuity, overtime premiums and holiday premiums use **basic**.
- **CR 31(2) vs amended DL 54(4):** possible inconsistency on the 14-day referral deadline.

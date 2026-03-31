# Representative endpoint catalog

This skill keeps a representative catalog for each major OpenDART family.

| Name | Family | Path |
|---|---|---|
| corp_code | 공시정보 | `/api/corpCode.xml` |
| company_overview | 공시정보 | `/api/company.json` |
| disclosure_list | 공시정보 | `/api/list.json` |
| document_download | 공시정보 | `/api/document.xml` |
| dividend_info | 정기보고서 주요정보 | `/api/alotMatter.json` |
| executive_status | 정기보고서 주요정보 | `/api/exctvSttus.json` |
| employee_status | 정기보고서 주요정보 | `/api/empSttus.json` |
| single_company_financials | 정기보고서 재무정보 | `/api/fnlttSinglAcnt.json` |
| single_company_index | 정기보고서 재무정보 | `/api/fnlttSinglIndx.json` |
| financial_xbrl | 정기보고서 재무정보 | `/api/fnlttXbrl.xml` |
| financial_multiple_index | 활용마당 | `/api/fnlttCmpnyIndx.json` |
| major_shareholding | 지분공시 종합정보 | `/api/majorstock.json` |
| executive_ownership | 지분공시 종합정보 | `/api/elestock.json` |
| default_occurrence | 주요사항보고서 주요정보 | `/api/dfOcr.json` |
| overseas_listing | 주요사항보고서 주요정보 | `/api/ovLst.json` |
| equity_registration | 증권신고서 주요정보 | `/api/estkRs.json` |
| bond_registration | 증권신고서 주요정보 | `/api/bdRs.json` |

Use `python3 skills/opendart/scripts/opendart_cli.py endpoint` for script-readable output.

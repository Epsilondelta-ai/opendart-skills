from __future__ import annotations

from dataclasses import dataclass

EXPECTED_GUIDE_FAMILIES = (
    "공시정보",
    "정기보고서 주요정보",
    "정기보고서 재무정보",
    "활용마당",
    "지분공시 종합정보",
    "주요사항보고서 주요정보",
    "증권신고서 주요정보",
)


@dataclass(frozen=True)
class EndpointSpec:
    name: str
    family: str
    section: str
    path: str
    output: str
    required_params: tuple[str, ...]
    description: str
    source_url: str


ENDPOINTS: dict[str, EndpointSpec] = {
    "corp_code": EndpointSpec("corp_code", "공시정보", "overview", "/api/corpCode.xml", "binary", ("crtfc_key",), "공시 대상 법인의 고유번호 ZIP/XML 다운로드", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018"),
    "company_overview": EndpointSpec("company_overview", "공시정보", "overview", "/api/company.json", "json", ("crtfc_key", "corp_code"), "기업 개황 조회", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002"),
    "disclosure_list": EndpointSpec("disclosure_list", "공시정보", "disclosures", "/api/list.json", "json", ("crtfc_key",), "공시 목록/검색", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001"),
    "document_download": EndpointSpec("document_download", "공시정보", "disclosures", "/api/document.xml", "binary", ("crtfc_key", "rcept_no"), "원문 공시문서 다운로드", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019007"),
    "dividend_info": EndpointSpec("dividend_info", "정기보고서 주요정보", "periodic-reports", "/api/alotMatter.json", "json", ("crtfc_key", "corp_code", "bsns_year", "reprt_code"), "배당에 관한 사항", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019005"),
    "executive_status": EndpointSpec("executive_status", "정기보고서 주요정보", "periodic-reports", "/api/exctvSttus.json", "json", ("crtfc_key", "corp_code", "bsns_year", "reprt_code"), "임원 현황", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019010"),
    "employee_status": EndpointSpec("employee_status", "정기보고서 주요정보", "periodic-reports", "/api/empSttus.json", "json", ("crtfc_key", "corp_code", "bsns_year", "reprt_code"), "직원 현황", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019011"),
    "single_company_financials": EndpointSpec("single_company_financials", "정기보고서 재무정보", "financials", "/api/fnlttSinglAcnt.json", "json", ("crtfc_key", "corp_code", "bsns_year", "reprt_code", "fs_div"), "단일회사 주요계정 조회", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016"),
    "single_company_index": EndpointSpec("single_company_index", "정기보고서 재무정보", "financials", "/api/fnlttSinglIndx.json", "json", ("crtfc_key", "corp_code", "bsns_year", "reprt_code", "idx_cl_code"), "단일회사 주요 재무지표", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022001"),
    "financial_xbrl": EndpointSpec("financial_xbrl", "정기보고서 재무정보", "financials", "/api/fnlttXbrl.xml", "binary", ("crtfc_key", "rcept_no"), "XBRL 재무제표 원문 다운로드", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019019"),
    "financial_multiple_index": EndpointSpec("financial_multiple_index", "활용마당", "financials", "/api/fnlttCmpnyIndx.json", "json", ("crtfc_key", "corp_code", "bsns_year", "reprt_code", "idx_cl_code"), "회사간 주요 재무지표 비교", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022002"),
    "major_shareholding": EndpointSpec("major_shareholding", "지분공시 종합정보", "equity", "/api/majorstock.json", "json", ("crtfc_key", "corp_code"), "대량보유 상황보고", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019021"),
    "executive_ownership": EndpointSpec("executive_ownership", "지분공시 종합정보", "equity", "/api/elestock.json", "json", ("crtfc_key", "corp_code"), "임원·주요주주 소유보고", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019022"),
    "default_occurrence": EndpointSpec("default_occurrence", "주요사항보고서 주요정보", "material-events", "/api/dfOcr.json", "json", ("crtfc_key", "corp_code", "bgn_de", "end_de"), "부도발생 주요사항보고서", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020019"),
    "overseas_listing": EndpointSpec("overseas_listing", "주요사항보고서 주요정보", "material-events", "/api/ovLst.json", "json", ("crtfc_key", "corp_code", "bgn_de", "end_de"), "해외 증권시장 주권등 상장", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020031"),
    "equity_registration": EndpointSpec("equity_registration", "증권신고서 주요정보", "registration", "/api/estkRs.json", "json", ("crtfc_key", "corp_code", "bgn_de", "end_de"), "지분증권 증권신고서 요약", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020054"),
    "bond_registration": EndpointSpec("bond_registration", "증권신고서 주요정보", "registration", "/api/bdRs.json", "json", ("crtfc_key", "corp_code", "bgn_de", "end_de"), "채무증권 증권신고서 요약", "https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020055"),
}

FAMILY_TO_SECTION = {
    "공시정보": "disclosures",
    "정기보고서 주요정보": "periodic-reports",
    "정기보고서 재무정보": "financials",
    "활용마당": "financials",
    "지분공시 종합정보": "equity",
    "주요사항보고서 주요정보": "material-events",
    "증권신고서 주요정보": "registration",
}


def get_endpoint(name: str) -> EndpointSpec:
    return ENDPOINTS[name]


def list_endpoints(*, family: str | None = None, section: str | None = None) -> list[EndpointSpec]:
    items = list(ENDPOINTS.values())
    if family is not None:
        items = [item for item in items if item.family == family]
    if section is not None:
        items = [item for item in items if item.section == section]
    return sorted(items, key=lambda item: item.name)

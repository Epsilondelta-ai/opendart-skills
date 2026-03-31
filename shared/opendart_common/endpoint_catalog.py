from __future__ import annotations

from dataclasses import dataclass

CATALOG_SPLIT_THRESHOLD = 40
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
    skill: str
    path: str
    output: str
    required_params: tuple[str, ...]
    description: str
    source_url: str


ENDPOINTS: dict[str, EndpointSpec] = {
    "corp_code": EndpointSpec(
        name="corp_code",
        family="공시정보",
        skill="opendart",
        path="/api/corpCode.xml",
        output="binary",
        required_params=("crtfc_key",),
        description="공시 대상 법인의 고유번호 ZIP/XML 다운로드",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019018",
    ),
    "company_overview": EndpointSpec(
        name="company_overview",
        family="공시정보",
        skill="opendart",
        path="/api/company.json",
        output="json",
        required_params=("crtfc_key", "corp_code"),
        description="기업 개황 조회",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019002",
    ),
    "disclosure_list": EndpointSpec(
        name="disclosure_list",
        family="공시정보",
        skill="opendart-disclosures",
        path="/api/list.json",
        output="json",
        required_params=("crtfc_key",),
        description="공시 목록/검색",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019001",
    ),
    "document_download": EndpointSpec(
        name="document_download",
        family="공시정보",
        skill="opendart-disclosures",
        path="/api/document.xml",
        output="binary",
        required_params=("crtfc_key", "rcept_no"),
        description="원문 공시문서 다운로드",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS001&apiId=2019007",
    ),
    "dividend_info": EndpointSpec(
        name="dividend_info",
        family="정기보고서 주요정보",
        skill="opendart-periodic-reports",
        path="/api/alotMatter.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bsns_year", "reprt_code"),
        description="배당에 관한 사항",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019005",
    ),
    "executive_status": EndpointSpec(
        name="executive_status",
        family="정기보고서 주요정보",
        skill="opendart-periodic-reports",
        path="/api/exctvSttus.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bsns_year", "reprt_code"),
        description="임원 현황",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019010",
    ),
    "employee_status": EndpointSpec(
        name="employee_status",
        family="정기보고서 주요정보",
        skill="opendart-periodic-reports",
        path="/api/empSttus.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bsns_year", "reprt_code"),
        description="직원 현황",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS002&apiId=2019011",
    ),
    "single_company_financials": EndpointSpec(
        name="single_company_financials",
        family="정기보고서 재무정보",
        skill="opendart-financials",
        path="/api/fnlttSinglAcnt.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bsns_year", "reprt_code", "fs_div"),
        description="단일회사 주요계정 조회",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019016",
    ),
    "single_company_index": EndpointSpec(
        name="single_company_index",
        family="정기보고서 재무정보",
        skill="opendart-financials",
        path="/api/fnlttSinglIndx.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bsns_year", "reprt_code", "idx_cl_code"),
        description="단일회사 주요 재무지표",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2022001",
    ),
    "financial_xbrl": EndpointSpec(
        name="financial_xbrl",
        family="정기보고서 재무정보",
        skill="opendart-financials",
        path="/api/fnlttXbrl.xml",
        output="binary",
        required_params=("crtfc_key", "rcept_no"),
        description="XBRL 재무제표 원문 다운로드",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS003&apiId=2019019",
    ),
    "major_shareholding": EndpointSpec(
        name="major_shareholding",
        family="지분공시 종합정보",
        skill="opendart-equity",
        path="/api/majorstock.json",
        output="json",
        required_params=("crtfc_key", "corp_code"),
        description="대량보유 상황보고",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019021",
    ),
    "executive_ownership": EndpointSpec(
        name="executive_ownership",
        family="지분공시 종합정보",
        skill="opendart-equity",
        path="/api/elestock.json",
        output="json",
        required_params=("crtfc_key", "corp_code"),
        description="임원·주요주주 소유보고",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS004&apiId=2019022",
    ),
    "default_occurrence": EndpointSpec(
        name="default_occurrence",
        family="주요사항보고서 주요정보",
        skill="opendart-material-events",
        path="/api/dfOcr.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bgn_de", "end_de"),
        description="부도발생 주요사항보고서",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020019",
    ),
    "overseas_listing": EndpointSpec(
        name="overseas_listing",
        family="주요사항보고서 주요정보",
        skill="opendart-material-events",
        path="/api/ovLst.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bgn_de", "end_de"),
        description="해외 증권시장 주권등 상장",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS005&apiId=2020031",
    ),
    "equity_registration": EndpointSpec(
        name="equity_registration",
        family="증권신고서 주요정보",
        skill="opendart-registration",
        path="/api/estkRs.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bgn_de", "end_de"),
        description="지분증권 증권신고서 요약",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020054",
    ),
    "bond_registration": EndpointSpec(
        name="bond_registration",
        family="증권신고서 주요정보",
        skill="opendart-registration",
        path="/api/bdRs.json",
        output="json",
        required_params=("crtfc_key", "corp_code", "bgn_de", "end_de"),
        description="채무증권 증권신고서 요약",
        source_url="https://opendart.fss.or.kr/guide/detail.do?apiGrpCd=DS006&apiId=2020055",
    ),
}

FAMILY_TO_SKILL = {
    "공시정보": "opendart-disclosures",
    "정기보고서 주요정보": "opendart-periodic-reports",
    "정기보고서 재무정보": "opendart-financials",
    "활용마당": "opendart-financials",
    "지분공시 종합정보": "opendart-equity",
    "주요사항보고서 주요정보": "opendart-material-events",
    "증권신고서 주요정보": "opendart-registration",
}


def get_endpoint(name: str) -> EndpointSpec:
    return ENDPOINTS[name]


def list_endpoints(*, family: str | None = None, skill: str | None = None) -> list[EndpointSpec]:
    items = list(ENDPOINTS.values())
    if family is not None:
        items = [item for item in items if item.family == family]
    if skill is not None:
        items = [item for item in items if item.skill == skill]
    return sorted(items, key=lambda item: item.name)

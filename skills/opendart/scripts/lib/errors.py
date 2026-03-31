from __future__ import annotations

STATUS_LABELS = {
    "000": "정상",
    "010": "등록되지 않은 키",
    "011": "사용할 수 없는 키",
    "012": "접근할 수 없는 IP",
    "013": "조회된 데이터 없음",
    "014": "파일이 존재하지 않음",
    "020": "요청 제한 초과",
    "021": "조회 가능한 회사 수 초과",
    "100": "부적절한 필드 값",
    "101": "부적절한 접근",
    "800": "시스템 점검 중",
    "900": "정의되지 않은 오류",
    "901": "개인정보 보유기간 만료 계정",
}


class OpenDartAPIError(RuntimeError):
    def __init__(self, status: str, message: str, payload: object | None = None):
        self.status = status
        self.payload = payload
        super().__init__(f"[{status}] {message}")


def describe_status(status: str) -> str:
    return STATUS_LABELS.get(str(status), "알 수 없는 상태 코드")


def ensure_success(payload: dict) -> dict:
    status = str(payload.get("status", "000"))
    if status != "000":
        message = payload.get("message") or describe_status(status)
        raise OpenDartAPIError(status=status, message=str(message), payload=payload)
    return payload

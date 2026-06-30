from functools import lru_cache

from app.agent.graph import DiagnosisAgent
from app.core.config import get_settings
from app.devices.service import DeviceService
from app.diagnoses.repository import InMemoryDiagnosisRepository
from app.diagnoses.service import DiagnosisService
from app.knowledge.repository import FixtureKnowledgeRepository
from app.log_analysis.service import LogAnalysisService
from app.log_collection.readers import FixtureLogReader, SSHLogReader
from app.log_collection.service import LogCollectionService
from app.retrieval.service import RetrievalService


@lru_cache
def get_diagnosis_service() -> DiagnosisService:
    settings = get_settings()
    log_reader = SSHLogReader() if settings.log_reader_mode == "ssh" else FixtureLogReader()

    device_service = DeviceService()
    log_collection = LogCollectionService(log_reader)
    log_analysis = LogAnalysisService()
    retrieval = RetrievalService(FixtureKnowledgeRepository())
    agent = DiagnosisAgent(device_service, log_collection, log_analysis, retrieval)

    return DiagnosisService(InMemoryDiagnosisRepository(), agent)


_A=None
import dataclasses
from localstack.utils.strings import short_uid
@dataclasses.dataclass
class ApiResponse:
	success:bool=True
	def to_dict(A):return dataclasses.asdict(A)
@dataclasses.dataclass
class QueryResponseData:queryId:str=dataclasses.field(default_factory=short_uid);rowtype:list=dataclasses.field(default_factory=list);rowset:list=dataclasses.field(default_factory=list);rowsetBase64:str=_A;chunks:list=dataclasses.field(default_factory=list);chunkHeaders:dict=dataclasses.field(default_factory=dict);total:int=0;parameters:list[dict]=dataclasses.field(default_factory=list);queryResultFormat:str=_A;command:str=_A;src_locations:list[str]=_A;stageInfo:dict=_A;sourceCompression:str=_A
@dataclasses.dataclass
class QueryResponse(ApiResponse):data:QueryResponseData=dataclasses.field(default_factory=QueryResponseData)
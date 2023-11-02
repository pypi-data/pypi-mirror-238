
from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func,text
from sqlalchemy.future import select
from typing import TypeVar,Tuple,List,Dict,Any,Union,Iterator
from sqlalchemy .orm.attributes import InstrumentedAttribute
from sqlalchemy.engine.row import  Row
from  sqlalchemy.engine.result import ScalarResult,ChunkedIteratorResult
from sqlalchemy.sql.elements import ColumnElement
from sqlalchemy.sql import Select
from .db_filter import absFilterItems


#from sqlalchemy.orm import selectinload # 紧急装载器 在该表主键又外键的基础上使用 select(UserTable).options(selectinload(UserTable.LoginLog))
 
from co6co.utils import log

class DbOperations:
	def __init__(self,db_session:AsyncSession) -> None:
		self.db_session = db_session
		pass
	@staticmethod
	def remove_db_instance_state( poInstance_or_poList:Iterator| Any )->List[Dict]|Dict:
		if  hasattr (poInstance_or_poList,"__iter__"): return [dict(filter(lambda k: k[0] !="_sa_instance_state", a1.__dict__.items())) for a1 in poInstance_or_poList]  
		else: return dict(filter(lambda k: k[0] !="_sa_instance_state", poInstance_or_poList.__dict__.items()))

	async def _get_one(self, select:select, selectField:bool=True):
		"""
		获取一行数据
		存在多行,返回第一行
		为None 返回None
		""" 
		try: 
			data=await self.db_session.execute(select)
			if selectField:
				#row=data.one_or_none() # 没有返回None， 多行 异常Multiple rows were found when one or none was required
				row=data.fetchone() 	# 没有返回None， 多行，选一行给你
				if row==None:return row 
				return dict(zip(row._fields,row)) 
			else:
				row:Row=data.fetchone()  
				if row==None:return row
				return row[0]
		except Exception as e:
			log.warn(f"在未找到!\terror:{e}")
			return None
		
	async def _get_scalar(self ,select:select)->Any:
		data=await self.db_session.execute(select)
		return data.scalar()
	 
	async def _get_tuple(self ,select:select)-> list:  
		#sqlalchemy.engine.result.ChunkedIteratorResult
		data=await self.db_session.execute(select) 
		return [dict(zip(a._fields,a))  for a in  data]

	async def _get_list(self, select:select)-> list:  
		data=await self.db_session.execute(select) 
		return self.remove_db_instance_state(data.scalars().fetchall())  
	
	async def get_one(self,selectColumnOrPo:TypeVar|Tuple[InstrumentedAttribute],*filters:ColumnElement[bool])->Any|None:
		"""
		获取一条数据
		返回 dict 或者 PO 实体
		"""
		'''result = await self.db_session.execute(text('select version()')) #通过conn对象就可对DB进行操作​ 
		data=result.fetchone() '''
		isTule,sml=self._create_select(selectColumnOrPo,*filters)
		return  await self._get_one(sml,isTule) 

	async def get_one_by_pk(self,po:TypeVar,pk:Union[Any, Tuple[Any, ...]]):
		"""
		通过 主键 获取实体
		"""
		try:
			one=await self.db_session.get_one(po,ident=pk) 
			return one
		except Exception as e:
			log.warn(f"在{po},查找：pk:{pk} 未找到!\terror:{e}")
			return None
	
	
	
	def _create_select(self,selectColumnOrPo:Tuple[InstrumentedAttribute]|TypeVar,*filters:ColumnElement[bool] ) ->  (bool,Select[Any]):
		isTule= type(selectColumnOrPo)==tuple or type(selectColumnOrPo)==list  
		if isTule:
			sml=select(*selectColumnOrPo).filter(and_(*filters))
		else:
			# {type(selectColumnOrPo)} == sqlalchemy.orm.decl_api.DeclarativeMeta 
			po:TypeVar=selectColumnOrPo
			sml=select(po).filter(and_(*filters))
		return isTule,sml 

	async def _create_paged_select(self,filterItem:absFilterItems, *selectColumn:InstrumentedAttribute,  allow_paged:bool=True, allow_order:bool=True)->  (bool,select):
		"""
		创建 Column select
		"""
		filters=filterItem.filter() 
		po_type=filterItem.po_type  
		#selectColumn 不会为 None
		isTule=len(selectColumn)>0
		if isTule: 
			isTule, sml= self._create_select(selectColumn,*filters)
			#sml=select(*selectColumn).filter(and_(*filters))
		else:
			isTule,sml = self._create_select(po_type,*filters)
			#sml=select(po_type).filter(and_(*filters))
		
		sml:Select[Any]=sml
		
		if allow_paged:
			limit=filterItem.limit
			offset=filterItem.offset
			sml=sml.offset(offset).limit(limit)
		if allow_order:
			orderBy=filterItem.getOrderBy()
			sml=sml.order_by(*orderBy)
		return isTule,sml
	
	async def text(self,text:text)->dict:
		"""
		执行文本sql,
		返回: dict
		"""
		data=await self.db_session.execute(select(text))  
		return [dict(zip(a._fields,a))  for a in  data] 
	
	async def get_list(self,selectColumnOrPo:Tuple[InstrumentedAttribute]|TypeVar,*filters:ColumnElement[bool]): 
		isTule,sml=self._create_select(selectColumnOrPo,*filters)
		if isTule:return await self._get_tuple(sml)
		return await self._get_list(sml)
	
	async def count(self,*filters:ColumnElement[bool],column:InstrumentedAttribute="*" )->int:
		return await self._get_scalar(select(func.count(column)).filter(and_(*filters))) 
	
	async def exist(self,*filters:ColumnElement[bool],column:InstrumentedAttribute="*" )->Any:
		return await self.count(*filters,column=column)>0
	
class DbPagedOperations(DbOperations): 
	def __init__(self, db_session:AsyncSession,filter_items:absFilterItems):
		super().__init__(db_session)
		self.filter_items=filter_items  
	
	async def get_count(self,field:InstrumentedAttribute="*" )->int:
		"""
		根据 absFilterItems 获取符合条件的条数
		"""
		filters=self.filter_items.filter()
		return await self.count(*filters,field)
		#return await self._get_scalar(select(func.count(field)).filter(and_(*filters)))
		'''
		execute =await self.db_session.execute(select(func.count(field)).filter(and_(*filters)))  
		total= execute.scalar()   '''
		
		'''from co6co.utils import log
		#当选取整个对象的时候，都要用 scalars 方法，否则返回的是一个包含一个对象的 tuple 
		bts=await self.db_session.execute(select(ProcessPO.id,ProcessPO.boatName,ProcessPO.flowStatus).filter(and_(*filters)).limit(3))
	 
		log.succ(f"-----{type(bts)}\n{dir(bts)}") 
		for b in bts.fetchall():
			print(b)  

		filters=self.filter_items.filter( )
		orderBy=self.filter_items.getOrderBy() 
		data=await self.db_session.execute(select(ProcessPO).filter(and_(*filters)).offset(self.filter_items. get_db_page_index()).limit(3).order_by(*orderBy))
		log.succ(f"-----{type(data)}\n{dir(data)}")
		for b in data:
			print(b.tuple)  

		one=await self.db_session.get_one(ProcessPO,ident=2884) 
		print(one) ''' 
		return total
	
	async def get_paged (self ,*selectColumn:InstrumentedAttribute|TypeVar==None)-> list:
		"""
		selectColumn:  实体对象或者 filed
		返回列表
		"""
		isTule,sml=await self._create_paged_select(self.filter_items,*selectColumn)
		if isTule:return await  self._get_tuple(sml)
		return await self._get_list(sml)
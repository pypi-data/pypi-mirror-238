from dataclasses import dataclass, field
from functools import partial, reduce, singledispatch, wraps
from pathlib import Path
from typing import (Any, AsyncGenerator, AsyncIterable, Awaitable, Callable,
                    Coroutine, Dict, Generic, Iterable, List, Literal, Mapping,
                    Optional, Sequence, Set, Tuple, TypeVar, Union, cast)

from jinja2 import Environment, FileSystemLoader, Template, select_autoescape
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module
from typing_extensions import ParamSpec

from .server import APIServer

T = TypeVar("T")
P = ParamSpec("P")

class NextRoute(BaseModel):
	"""
	NextRoute
	---------
	Decorator to document a function as a NextRoute.

	Parameters
	----------
	url : str
		URL for the AJAX request
	label : str
		Label to display inside the div
	class_name : str, optional
		CSS class to apply to the link, by default "next-route"
	tag : str, optional
		HTML tag to use for the link, by default "a"
	trigger : str, optional
		Event to trigger the AJAX request, by default "click"
	method : Literal["get","post","put","patch","delete"], optional
		HTTP method for the AJAX request, by default "get"
	target : str, optional
		DOM element selector to update with the response, by default "this"
	swap : Literal['outerHTML', 'innerHTML', 'beforebegin', 'afterbegin', 'beforeend', 'afterend', 'none', "delete"], optional
		How to update the DOM element with the response, by default "none"
	"""
	url: str = Field(..., description="URL for the AJAX request")
	label: str = Field(..., description="Label to display inside the div")
	class_name: str = Field(default="next-route", description="CSS class to apply to the link")
	tag: str = Field(default="a", description="HTML tag to use for the link")
	trigger: str = Field(default="click", description="Event to trigger the AJAX request")
	method: Literal["get","post","put","patch","delete"] = Field(default="get", description="HTTP method for the AJAX request")
	target: str = Field(default="this", description="DOM element selector to update with the response")
	swap: Literal['outerHTML', 'innerHTML', 'beforebegin', 'afterbegin', 'beforeend', 'afterend', 'none', "delete"] = Field(default="none", description="How to update the DOM element with the response")
	
	def __call__(self,func: Callable[P, Coroutine[Any, Any, Dict[str,Any]]]):
		"""
		Decorate a function as a NextRoute.
		"""
		
		@wraps(func)
		async def wrapper(*args: P.args, **kwargs: P.kwargs):
			context = await func(*args, **kwargs)
			next_link = self.dict()
			context["htmx"] = next_link
			return context
		return wrapper


class NextApp(APIServer):
	"""
	Aiohttp Application with automatic OpenAPI generation.
	"""
	@property
	def env(self) -> Environment:
		"""
		Template engine environment.
		"""
		return Environment(
			loader=FileSystemLoader("pages"),
			autoescape=select_autoescape(["html", "xml"]),
		   enable_async=True)

	
	def page(self, template:str):
		"""
		Renders a page.
		"""
		def decorator(func: Callable[P, Coroutine[Any, Any, Dict[str,Any]]]) ->Callable[P, Coroutine[Any, Any, str]]:
			@wraps(func)
			async def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:
				context = await func(*args, **kwargs)
				return await self.env.get_template(template).render_async(**context)
			return wrapper
		return decorator
	
		
	def component(self,func: Callable[P, Coroutine[Any, Any, Dict[str,Any]]]) ->Callable[P, Coroutine[Any, Any, str]]:
		"""
		Renders a Component baaed on a function docstring.
		"""
		@wraps(func)
		async def wrapper(*args: P.args, **kwargs: P.kwargs) -> str:  # type: ignore
			assert func.__doc__ is not None, f"Missing component template for {func.__name__}"
			func.__doc__ = """{% from "macros.html" import next %}""" + func.__doc__
			context = await func(*args, **kwargs)
			return await self.env.from_string(func.__doc__).render_async(**context)
		return wrapper
	

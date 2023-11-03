# -*- coding: utf-8 -*-
"""
Utilities for performing JSON-based IPC with standard input and output.
"""

from __future__ import annotations

from typing import Any, Iterator, List
import json
import sys


class _EmptyInputLine(Exception):
	pass


class JSONStandardIOIPC:
	__slots__ = (
		"max_line_count",
		"_line_buf",
		"_object_buf",
		"_dec",
		"_eof",
	)

	def __init__(self, max_line_count: int = 128, *args, **kwds) -> None:
		super().__init__(*args, **kwds)
		self._line_buf: List[str] = []
		self._object_buf: List[Any] = []
		self.max_line_count = max(1, max_line_count)
		self._dec = json.JSONDecoder()
		self._eof = False

	def _read(self) -> Any:
		if self._object_buf:
			return self._object_buf.pop(0)
		aux = sys.stdin.readline()
		# _log.debug("read: %r", aux)
		if not aux:
			self._eof = True
		aux = aux.strip()
		if not aux:
			raise _EmptyInputLine
		if self._line_buf:
			self._line_buf.append(aux)
			aux = "".join(self._line_buf)
		total_len = len(aux)
		while aux:
			try:
				parsed_obj, consumed_len = self._dec.raw_decode(aux)
			except json.JSONDecodeError:
				if not self._line_buf:
					self._line_buf.append(aux)
				raise
			self._object_buf.append(parsed_obj)
			aux = aux[consumed_len:].lstrip()
		consumed_len = total_len - len(aux)
		remain_lines = None
		if self._line_buf:
			acc_len = 0
			bound_idx = -1
			for idx, line_text in enumerate(self._line_buf):
				acc_len = acc_len + len(line_text)
				if acc_len >= consumed_len:
					bound_idx = idx + 1
					break
			if bound_idx < len(self._line_buf):
				remain_lines = self._line_buf[bound_idx:]
		self._line_buf = [aux] if aux else []
		if remain_lines:
			self._line_buf.extend(remain_lines)
		return self._object_buf.pop(0)

	def read(self) -> Any:
		while True:
			# _log.debug("current line buffer: %r", self._line_buf)
			try:
				result = self._read()
				return result
			except json.JSONDecodeError:
				pass
			except _EmptyInputLine:
				pass
			poped_line = False
			while len(self._line_buf) > self.max_line_count:
				self._line_buf.pop(0)
				poped_line = True
			if not self._eof:
				continue
			if not poped_line:
				self._line_buf.pop(0)
			if not self._line_buf:
				raise StopIteration

	def write(self, obj: Any) -> None:
		json.dump(obj, sys.stdout)
		sys.stdout.write("\n")
		sys.stdout.flush()

	def __iter__(self) -> Iterator:
		return self

	def __next__(self) -> Any:
		return self.read()

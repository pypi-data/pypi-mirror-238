#!/usr/bin/env python
"""
Stub-files for scipy.signal. This module contains the type-annotations for
scipy's library for fourier-transformations and signal analysis.
"""
from typing import Tuple, Optional, Union, overload, TypeVar

from scientific_plots.types_ import Vector, Matrix, Tensor


def welch(
    Y: Union[Vector, list[float]],
    fs: Optional[float] = None,
    scaling: str = "density",
    window: Optional[str] = "hamming",
    nperseg: int = 10,
    detrend: bool = False) -> Tuple[Vector, Vector]: ...


def periodogram(
    Y: Union[Vector, list[float]],
    fs: Optional[float] = None,
    scaling: str = "density",
    window: Optional[str] = "hamming",
    detrend: bool = False) -> Tuple[Vector, Vector]: ...


Single = Union[Vector, list[float]]
Double = Union[tuple[Vector, Vector], tuple[list[float], list[float]]]


@overload
def savgol_filter(
    x: Single, window_length: Union[int, float], polyorder: int,
    deriv: Optional[int] = None, delta: Optional[float] = None,
    mode: str = "nearest") -> Vector: ...


@overload
def savgol_filter(
    x: Double, window_length: Union[int, float], polyorder: int,
    deriv: Optional[int] = None, delta: Optional[float] = None,
    mode: str = "nearest")\
        -> tuple[Vector, Vector]: ...


def sosfilt(
    sos: Single, x: Single, axis: int = -1, zi: Optional[Single] = None,
    padtype: Optional[str] = "odd", padlen: Optional[int] = None)\
        -> Vector: ...


def sosfiltfilt(
    sos: Single, x: Single, axis: int = -1, zi: Optional[Single] = None,
    padtype: Optional[str] = "odd", padlen: Optional[int] = None)\
        -> Vector: ...


def butter(
    N: int, Wn: Single, btype: str = "low", analog: bool = False,
    output: str = "ba", fs: Optional[float] = None) -> Vector: ...


Input = TypeVar("Input", Vector, Matrix, Tensor)


def wiener(
    im: Input,
    noise: Optional[float] = None,
    mysize: Optional[Union[int, Vector]] = None) -> Input: ...

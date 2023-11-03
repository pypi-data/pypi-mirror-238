# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2022-12-19 20:06:20
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Multi task methods.
"""


from __future__ import annotations
from typing import Any, List, Tuple, Optional, Callable, Generator
from concurrent.futures import ThreadPoolExecutor, Future, as_completed


__all__ = (
    "RThreadPool",
)


class RThreadPool(object):
    """
    Rey's `thread pool` type.
    """


    def __init__(
        self,
        func: Callable,
        *args: Any,
        _max_workers: Optional[int] = None,
        **kwargs: Any
    ) -> None:
        """
        Build `thread pool` instance.

        Parameters
        ----------
        func : Thread task.
        args : Task default arguments.
        max_workers: Maximum number of threads.
            - `None` : Number of CPU + 4, 32 maximum.
            - `int` : Use this value, no maximum limit.

        kwargs : Task default keyword arguments.
        """

        # Set attribute.
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.thread_pool = ThreadPoolExecutor(
            _max_workers,
            func.__name__
        )
        self.futures: List[Future] = []


    def one(
        self,
        *args: Any,
        **kwargs: Any
    ) -> Future:
        """
        Add a task to the thread pool.

        Parameters
        ----------
        args : Task arguments, after default arguments.
        kwargs : Task keyword arguments, after default keyword arguments.

        Returns
        -------
        Task instance.
        """

        # Set parameter.
        func_args = (
            *self.args,
            *args
        )
        func_kwargs = {
            **self.kwargs,
            **kwargs
        }

        # Submit.
        future = self.thread_pool.submit(
            self.func,
            *func_args,
            **func_kwargs
        )

        # Save.
        self.futures.append(future)

        return future


    def batch(
        self,
        *args: Tuple,
        **kwargs: Tuple
    ) -> List[Future]:
        """
        Add a batch of tasks to the thread pool.
        parameters sequence will combine one by one, and discard excess parameters.

        Parameters
        ----------
        args : Sequence of task arguments, after default arguments.
        kwargs : Sequence of task keyword arguments, after default keyword arguments.

        Returns
        -------
        Task instance list.

        Examples
        --------
        >>> func = lambda *args, **kwargs: print(args, kwargs)
        >>> a = (1, 2)
        >>> b = (3, 4, 5)
        >>> c = (11, 12)
        >>> d = (13, 14, 15)
        >>> thread_pool = RThreadPool(func, 0, z=0)
        >>> thread_pool.batch(a, b, c, d)
        (0, 1, 3) {'z': 0, 'c': 11, 'd': 13}
        (0, 2, 4) {'z': 0, 'c': 12, 'd': 14}
        """

        # Combine.
        args_zip = zip(*args)
        kwargs_zip = zip(
            *[
                [
                    (key, value)
                    for value in values
                ]
                for key, values in kwargs.items()
            ]
        )
        params_zip = zip(args_zip, kwargs_zip)

        # Batch submit.
        futures = [
            self.one(*args_, **dict(kwargs_))
            for args_, kwargs_ in params_zip
        ]

        # Save.
        self.futures.extend(futures)

        return futures


    def generate(
        self,
        timeout: Optional[float] = None
    ) -> Generator[Future]:
        """
        Return the generator of added task instance.

        Parameters
        ----------
        timeout : Call generator maximum waiting seconds, timeout throw exception.
            - `None` : Infinite.
            - `float` : Set this seconds.

        Returns
        -------
        Generator of added task instance.
        """

        # Build.
        generator = as_completed(
            self.futures,
            timeout
        )

        return generator


    def repeat(
        self,
        number: int
    ) -> List[Future]:
        """
        Add a batch of tasks to the thread pool, and only with default parameters.

        Parameters
        ----------
        number : Number of add.

        Returns
        -------
        Task instance list.
        """

        # Batch submit.
        futures = [
            self.one()
            for n in range(number)
        ]

        # Save.
        self.futures.extend(futures)

        return futures


    __call__ = one


    __mul__ = repeat
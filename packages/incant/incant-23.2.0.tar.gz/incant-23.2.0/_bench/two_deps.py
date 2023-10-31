"""
Benchmark module for the `two_deps` scenario.

A function with two dependencies; the first depends on the other, and the other requires a parameter.
"""
from dependency_injector import containers, providers
from di.container import Container, bind_by_type
from di.dependent import Dependent
from di.executors import SyncExecutor
from wired import ServiceRegistry

from incant import Incanter


def dep2(input: str) -> float:
    return float(input) + 1


def dep1(dep2: float) -> int:
    return int(dep2) + 1


def func(dep1: int):
    return dep1 + 1


incant = Incanter()
incant.register_by_name(dep1)
incant.register_by_name(dep2)
prepared = incant.compose(func)


def incant_call_func():
    prepared("1")


# wired

service_registry = ServiceRegistry()
service_registry.register_factory(
    lambda container: dep2(container.get(name="input")), name="dep2"
)
service_registry.register_factory(
    lambda container: dep1(container.get(name="dep2")), name="dep1"
)
service_registry.register_factory(
    lambda container: func(container.get(name="dep1")), name="func"
)


def wired_call_func():
    container = service_registry.create_container()
    container.register_singleton("1", name="input")
    container.get(name="func")


# di

container = Container()
container.bind(bind_by_type(Dependent(dep1, scope="request"), int))
container.bind(bind_by_type(Dependent(dep2, scope="request"), float))
solved = container.solve(Dependent(func, scope="request"), scopes=["request"])
sync_executor = SyncExecutor()


def di_call_func():
    with container.enter_scope("request") as state:
        container.execute_sync(solved, sync_executor, state=state, values={str: "1"})


# Dependency-injector
class DepInjContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    func_factory = providers.Factory(
        func, dep1=providers.Factory(dep1, dep2=providers.Factory(dep2))
    )


dep_inj_container = DepInjContainer()
dep_inj_container.wire(modules=[__name__])


def dependency_injector_call_func():
    dep_inj_container.func_factory(dep1__dep2__input="1")

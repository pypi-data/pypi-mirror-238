import pytest
from retroapi import RetroApi


def test_valid_smiles():
    api = RetroApi()
    smiles = "COc1cccc(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    assert api.validate_smiles(smiles) is True
    smiles = "Cccccc1100(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    assert api.validate_smiles(smiles) is False

@pytest.mark.asyncio
async def test_avalid_smiles():
    api = RetroApi()
    smiles = "COc1cccc(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    res = await api.avalidate_smiles(smiles)
    assert res is True
    smiles = "Cccccc1100(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    res = await api.avalidate_smiles(smiles)
    assert res is False


def test_create_task():
    api = RetroApi()
    smiles = "COc1cccc(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    task_id = api.create_task(smiles)
    assert type(task_id) == str
    routes = api.get_routes(task_id)
    if routes is not None:
        route = routes[0]
        assert 'plausibility' in route

@pytest.mark.asyncio
async def test_acreate_task():
    api = RetroApi()
    smiles = "COc1cccc(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    task_id = await api.acreate_task(smiles)
    assert type(task_id) == str
    routes = await api.aget_routes(task_id)
    if routes is not None:
        route = routes[0]
        assert 'plausibility' in route

def test_stock():
    api = RetroApi()
    smiles = "COc1cccc(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    assert api.check_stock(smiles) is False
    smiles = "COc1cc(C=CC(=O)O)cc(OC)c1OC"
    assert api.check_stock(smiles) is True

@pytest.mark.asyncio
async def test_astock():
    api = RetroApi()
    smiles = "COc1cccc(OC(=O)/C=C/c2cc(OC)c(OC)c(OC)c2)c1"
    res = await api.acheck_stock(smiles)
    assert res is False
    smiles = "COc1cc(C=CC(=O)O)cc(OC)c1OC"
    res = await api.acheck_stock(smiles)
    assert res is True

def test_image():
    api = RetroApi()
    # reaction
    # smiles = "CC(=O)OC(C)=O.COc1cc(C=O)cc(OC)c1OC>>COc1cc(C=CC(=O)O)cc(OC)c1OC"
    smiles = "COc1cc(C=CC(=O)O)cc(OC)c1OC"  # reagent
    img_bytes = api.get_image_from_smiles(smiles)
    assert type(img_bytes) == bytes

@pytest.mark.asyncio
async def test_aimage():
    api = RetroApi()
    # reaction
    # smiles = "CC(=O)OC(C)=O.COc1cc(C=O)cc(OC)c1OC>>COc1cc(C=CC(=O)O)cc(OC)c1OC"
    smiles = "COc1cc(C=CC(=O)O)cc(OC)c1OC"  # reagent
    img_bytes = await api.aget_image_from_smiles(smiles)
    assert type(img_bytes) == bytes


def test_synthesis_task():
    api = RetroApi()
    products = "COc1cc(C(=O)O)cc(OC)c1OC"
    reactants = "C=CC(=O)O.COc1cc(Br)cc(OC)c1OC"
    syn_task = api.create_syn_task(products, reactants)
    assert type(syn_task) == str
    conditions = api.get_syn_conditions(syn_task)
    if conditions is not None:
        cond = conditions[0]
        assert "temperature" in cond
        assert "solvent" in cond

@pytest.mark.asyncio
async def test_asynthesis_task():
    api = RetroApi()
    products = "COc1cc(C(=O)O)cc(OC)c1OC"
    reactants = "C=CC(=O)O.COc1cc(Br)cc(OC)c1OC"
    syn_task = await api.acreate_syn_task(products, reactants)
    assert type(syn_task) == str
    conditions = await api.aget_syn_conditions(syn_task)
    if conditions is not None:
        cond = conditions[0]
        assert "temperature" in cond
        assert "solvent" in cond

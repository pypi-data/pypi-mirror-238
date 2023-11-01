import pytest
from retroapi import Name2Smiles



def test_name_2_smiles():
    name2smiles = Name2Smiles()
    chemical_name = "2,4,6-trinitrotoluene"
    smiles = name2smiles.get_smiles(chemical_name)
    assert smiles is not None
    assert smiles == "[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]"
    chemical_name = "4-Hydroxycoumarin"
    smiles = name2smiles.get_smiles(chemical_name)
    assert smiles is not None

@pytest.mark.asyncio
async def test_aname_2_smiles():
    name2smiles = Name2Smiles()
    chemical_name = "2,4,6-trinitrotoluene"
    smiles = await name2smiles.aget_smiles(chemical_name)
    assert smiles is not None
    assert smiles == "[N+](=O)([O-])C1=C(C)C(=CC(=C1)[N+](=O)[O-])[N+](=O)[O-]"
    chemical_name = "4-Hydroxycoumarin"
    smiles = await name2smiles.aget_smiles(chemical_name)
    assert smiles is not None

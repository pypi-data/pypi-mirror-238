import pytest
import peptacular_bindings


def test_get_modifications():
    assert peptacular_bindings.get_modifications_py('PEPTIDE') == {}
    assert peptacular_bindings.get_modifications_py('[Acetyl]PEPTIDE') == {-1: 'Acetyl'}
    assert peptacular_bindings.get_modifications_py('PEPTIDE[Acetyl]') == {7: 'Acetyl'}
    assert peptacular_bindings.get_modifications_py('P(1)EPTIDE') == {0:'1'}


def test_strip_modifications():
    assert peptacular_bindings.strip_modifications_py('PEPTIDE') == 'PEPTIDE'
    assert peptacular_bindings.strip_modifications_py('[Acetyl]PEPTIDE') == 'PEPTIDE'
    assert peptacular_bindings.strip_modifications_py('PEPTIDE[Acetyl]') == 'PEPTIDE'
    assert peptacular_bindings.strip_modifications_py('P(1)EPTIDE') == 'PEPTIDE'


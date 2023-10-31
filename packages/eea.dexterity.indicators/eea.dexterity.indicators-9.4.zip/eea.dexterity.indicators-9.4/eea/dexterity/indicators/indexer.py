""" indexer.py """
from plone.indexer import indexer
from zope.component import queryAdapter
from eea.dexterity.indicators.interfaces import IIndicator
from eea.dexterity.indicators.interfaces import IIndicatorMetadata


@indexer(IIndicator)
def data_provenance_indexer(obj):
    """Data Provenance indexer"""
    metadata = queryAdapter(obj, IIndicatorMetadata)
    if not metadata:
        return None
    data_provenance = getattr(metadata, "data_provenance", {})
    if not data_provenance or "data" not in data_provenance:
        return None

    data = {}
    for val in data_provenance['data']:
        org = val.get("organisation", "")
        if org:
            data[org] = org
    return data


@indexer(IIndicator)
def temporal_coverage_indexer(obj):
    """Temporal coverage indexer"""

    metadata = queryAdapter(obj, IIndicatorMetadata)
    if not metadata:
        return None
    temporal_coverage = getattr(metadata, "temporal_coverage", {})
    if not temporal_coverage or "temporal" not in temporal_coverage:
        return None

    data = {}
    for val in temporal_coverage["temporal"]:
        value = val.get("value", "")
        label = val.get("label", "")
        if value and label:
            data[value] = label
    return data

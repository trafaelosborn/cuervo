"""Caption edits isolated from the figures and all earlier edition builders."""
from reportlab.platypus import Paragraph, KeepTogether, Table

# Keys use figure identity, then exact pre-normalization text. Only prose changes.
EDITS = {
 'simultaneous-change': {
  " The stock notice does not establish the lumberyard's closing date.": '',
 },
 'cuervo-map': {
  ' This is a spatial relationship, not a dated reconstruction of the 1903 premises.': '',
 },
 'trade-notices': {
  ' A separate notice of a purchase of more than 4,000 sheep is not treated as the fourteen-car shipment.': '',
 },
 'trade-connections': {
  'The arrows represent separate observations, not consignments followed through Cuervo or shares of total trade.':
   'Arrows link separately documented transactions; they do not trace single consignments through Cuervo.',
 },
 'county-livestock': {
  'Markers show seven census observations, not an annual series or Cuervo totals.':
   'Markers show seven county census observations.',
 },
 'school-staff-and-care': {
  ' The notices do not establish when instruction resumed or which improvements were completed.': '',
 },
 'school-parcel': {
  ' It does not establish the construction date or connect this footprint to the 1912 school.': '',
 },
 'doctor-support': {
  'The report identifies an attempt to organize dependable support. It supplies no collected fund, medical appointment or agreed treatment fees.': '',
  'The proposed locality and contributor pool should not be equated with Cuervo resident households.':
   'Terry sought contributors across the newspaper’s locality.',
 },
 'people-and-households': {
  'These are reconstructed groups, not new houses or migrant families.':
   'Groups are reconstructed around the listed household heads.',
 },
 'work-under-one-roof': {
  " The instructor's workplace is not named.": '',
 },
 'regional-households': {
  ' Subtracting institutional residents does not estimate the city without its institutions.': '',
 },
 'journeys': {
  ' Railway mileages are not road distances.': '',
 },
 'retail': {
  "These are the census's retail categories, not all businesses or an estimate of Cuervo spending captured by Santa Rosa.":
   'The census’s retail classification includes some services and repairs.',
 },
 'station-book': {
  'The table describes administration; it does not count shipments.':
   'The table records freight administration.',
  ' Retained codes do not prove usable stockyards or livestock traffic.': '',
 },
 'dot-town': {
  ' Building labels and construction instructions are distinct from evidence of continued trading or completed demolition.': '',
 },
 'dot-details': {
  ' Those instructions do not by themselves identify occupied businesses displaced by construction.': '',
 },
 'dot-access': {
  ' These are provisions for access and wayfinding; they do not count travelers who stopped.': '',
  ' The drawings establish the specified connections and signs, not their opening or installation dates.': '',
 },
 'functional-chronology': {
  ' The events do not form an established chain of causes.': '',
 },
 'support': {
  'Shared-cost savings and the final closure are unmeasured.': '',
  'Reason for departure and actual resumption are unknown.': '',
  'Subscriptions and recruitment are not established.': '',
  'Her account does not establish the final issue date.': '',
  'The rows compare sources of support and observed decisions, not financial performance on a common scale. A proposal, an announcement and a completed withdrawal have different evidential status.':
   'Each row identifies an activity’s support and the dated observation or proposal concerning it.',
 },
 'church': {
  'Neither supplies local attendance, event venue or service frequency.':
   'The entry does not identify the event venue or attendance.',
 },
}

def edit_figure(items, key):
    replacements = EDITS.get(key, {})
    counts = {old: 0 for old in replacements}
    def visit(flow):
        if isinstance(flow, Paragraph):
            text = flow.text
            for old, new in replacements.items():
                counts[old] += text.count(old)
                text = text.replace(old, new)
            if not text.strip(): return None
            if text != flow.text:
                new = Paragraph(text, flow.style)
                for k, v in vars(flow).items():
                    if k.startswith('book_'): setattr(new, k, v)
                return new
        elif isinstance(flow, KeepTogether):
            flow._content = [y for x in flow._content if (y := visit(x)) is not None]
        elif isinstance(flow, Table):
            for row in flow._cellvalues:
                for i, cell in enumerate(row):
                    if isinstance(cell, list): row[i] = [y for x in cell if (y := visit(x)) is not None]
                    elif isinstance(cell, (Paragraph, KeepTogether, Table)): row[i] = visit(cell) or ''
        return flow
    result = [y for x in items if (y := visit(x)) is not None]
    assert all(c == 1 for c in counts.values()), (key, counts)
    return result

// -- Table --

function drawTable(sEDF, sFIFO, sRand) {
	const best = Math.min(sEDF.totalPen, sFIFO.totalPen, sRand.totalPen);
	const rows = [
		{ s: sEDF,  badge: 'badge-edf',  label: 'EDF' },
		{ s: sFIFO, badge: 'badge-fifo', label: 'FIFO' },
		{ s: sRand, badge: 'badge-rand', label: 'Random' },
	];
	document.getElementById('stats-table').innerHTML = rows.map(r => `
		<tr class="${r.s.totalPen === best ? 'best' : ''}">
			<td><span class="badge ${r.badge}">${r.label}</span></td>
			<td>${r.s.lateCount}</td>
			<td>${r.s.latePct}%</td>
			<td>${r.s.maxLat}</td>
			<td>R$ ${r.s.totalPen.toLocaleString('pt-BR')}</td>
		</tr>`).join('');
}

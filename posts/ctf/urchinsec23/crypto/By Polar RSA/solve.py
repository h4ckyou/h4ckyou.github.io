import gmpy2

n = 13660434380581469341975259828359442143257638335184201302273368295115642264434078009719568658893902099636280367748794936198883121916566759980319478068451889149773226303724397129080256671084001239425357663205345604232700769511136087038814886708523857954047161710079081105648157438922135347302268392557280337962501293170357378150549402374842219641781167567899043267569898951833055690878240668548807574813621152068811079565478546974052540054707402886449015640286146318337170863094022162781259688095263640720121736648132174258723707789668493418719055328110579315482197651253358684859047225130074022770557785786256404214699
e = 65537
c = 6871628831387254845533768683960373162341242116989102932644424168516685398490688896090738165409500155893271829821175645531448483724420092925032601186457766887212168440290133800336905932826679265026124645876063349409417889305954213241618291932972695529758465346545772616241655043046254951393408609775875051596401061060100988980412715973443220697998825095738335226176101757665864718900559469067798565041853075095199227165689645686676230586964611157933639511411797985832121378313546606701249613755067928341124819669691901860334342161683805978341664854908235664359495115685302794801118979227392641652990655667977367731767

a = gmpy2.iroot(n, 2)[0] + 1
b = a*a - n
while not gmpy2.iroot(b, 2)[1]:
    print(b)
    b = a*a - n
    a += 1

p = a - gmpy2.iroot(b, 2)[0]
q = n // p
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)
m = format(m, 'x')
for i in range(0, len(m), 2):
    print(chr(int(m[i:i+2], 16)), end='')
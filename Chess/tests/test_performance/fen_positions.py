try:
    from src.constants.constColours import *

except:
    from src.constants.constColours import *


KAUFMAN_TEST_SUITE = [
    {
        "fen": "1rbq1rk1/p1b1nppp/1p2p3/8/1B1pN3/P2B4/1P3PPP/2RQ1R1K w - - 0 1",
        "best_move": "Nf6+",
        "id": "K.01",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "3r2k1/p2r1p1p/1p2p1p1/q4n2/3P4/PQ5P/1P1RNPP1/3R2K1 b - - 0 1",
        "best_move": "Nxd4",
        "id": "K.02",
        "evaluation_favours": BLACK
    },
    {
        "fen": "3r2k1/1p3ppp/2pq4/p1n5/P6P/1P6/1PB2QP1/1K2R3 w - - 0 1",
        "avoid_move": "Rd1",
        "best_move": "Qf5",
        "id": "K.03",
        "evaluation_favours": BLACK
    },
    {
        "fen": "r1b1r1k1/1ppn1p1p/3pnqp1/8/p1P1P3/5P2/PbNQNBPP/1R2RB1K w - - 0 1",
        "best_move": "Rxb2",
        "id": "K.04",
        "evaluation_favours": WHITE
    },
    {
        "fen": "2r4k/pB4bp/1p4p1/6q1/1P1n4/2N5/P4PPP/2R1Q1K1 b - - 0 1",
        "best_move": "Qxc1",
        "id": "K.05",
        "evaluation_favours": BLACK
    },
    {
        "fen": "r5k1/3n1ppp/1p6/3p1p2/3P1B2/r3P2P/PR3PP1/2R3K1 b - - 0 1",
        "avoid_move": "Rxa2",
        "id": "K.06",
        "evaluation_favours": WHITE
    },
    {
        "fen": "2r2rk1/1bqnbpp1/1p1ppn1p/pP6/N1P1P3/P2B1N1P/1B2QPP1/R2R2K1 b - - 0 1",
        "best_move": "Bxe4",
        "id": "K.07",
        "evaluation_favours": BLACK
    },
    {
        "fen": "5r1k/6pp/1n2Q3/4p3/8/7P/PP4PK/R1B1q3 b - - 0 1",
        "best_move": "h6",
        "id": "K.08",
        "evaluation_favours": BOTH
    },
    {
        "fen": "r3k2r/pbn2ppp/8/1P1pP3/P1qP4/5B2/3Q1PPP/R3K2R w KQkq - 0 1",
        "best_move": "Be2",
        "id": "K.09",
        "evaluation_favours": WHITE
    },
    {
        "fen": "3r2k1/ppq2pp1/4p2p/3n3P/3N2P1/2P5/PP2QP2/K2R4 b - - 0 1",
        "best_move": "Nxc3",
        "id": "K.10",
        "evaluation_favours": BLACK
    },
    {
        "fen": "q3rn1k/2QR4/pp2pp2/8/P1P5/1P4N1/6n1/6K1 w - - 0 1",
        "best_move": "Nf5",
        "id": "K.11",
        "evaluation_favours": WHITE
    },
    {
        "fen": "6k1/p3q2p/1nr3pB/8/3Q1P2/6P1/PP5P/3R2K1 b - - 0 1",
        "best_move": "Rd6",
        "id": "K.12",
        "evaluation_favours": BOTH
    },
    {
        "fen": "1r4k1/7p/5np1/3p3n/8/2NB4/7P/3N1RK1 w - - 0 1",
        "best_move": "Nxd5",
        "id": "K.13",
        "evaluation_favours": WHITE
    },
    {
        "fen": "1r2r1k1/p4p1p/6pB/q7/8/3Q2P1/PbP2PKP/1R3R2 w - - 0 1",
        "best_move": "Rxb2",
        "id": "K.14",
        "evaluation_favours": WHITE
    },
    {
        "fen": "r2q1r1k/pb3p1p/2n1p2Q/5p2/8/3B2N1/PP3PPP/R3R1K1 w - - 0 1",
        "best_move": "Bxf5",
        "id": "K.15",
        "evaluation_favours": WHITE
    },
    {
        "fen": "8/4p3/p2p4/2pP4/2P1P3/1P4k1/1P1K4/8 w - - 0 1",
        "best_move": "b4",
        "id": "K.16",
        "evaluation_favours": WHITE
    },
    {
        "fen": "1r1q1rk1/p1p2pbp/2pp1np1/6B1/4P3/2NQ4/PPP2PPP/3R1RK1 w - - 0 1",
        "best_move": "e5",
        "id": "K.17",
        "evaluation_favours": WHITE
    },
    {
        "fen": "q4rk1/1n1Qbppp/2p5/1p2p3/1P2P3/2P4P/6P1/2B1NRK1 b - - 0 1",
        "best_move": "Qc8",
        "id": "K.18",
        "evaluation_favours": BLACK
    },
    {
        "fen": "r2q1r1k/1b1nN2p/pp3pp1/8/Q7/PP5P/1BP2RPN/7K w - - 0 1",
        "best_move": "Qxd7",
        "id": "K.19",
        "evaluation_favours": WHITE
    },
    {
        "fen": "8/5p2/pk2p3/4P2p/2b1pP1P/P3P2B/8/7K w - - 0 1",
        "best_move": "Bg4",
        "id": "K.20",
        "evaluation_favours": WHITE
    },
    {
        "fen": "8/2k5/4p3/1nb2p2/2K5/8/6B1/8 w - - 0 1",
        "best_move": "Kxb5",
        "id": "K.21",
        "evaluation_favours": BLACK
    },
    {
        "fen": "1B1b4/7K/1p6/1k6/8/8/8/8 w - - 0 1",
        "best_move": "Ba7",
        "id": "K.22",
        "evaluation_favours": BLACK
    },
    {
        "fen": "rn1q1rk1/1b2bppp/1pn1p3/p2pP3/3P4/P2BBN1P/1P1N1PP1/R2Q1RK1 b - - 0 1",
        "best_move": "Ba6",
        "id": "K.23",
        "evaluation_favours": WHITE
    },
    {
        "fen": "8/p1ppk1p1/2n2p2/8/4B3/2P1KPP1/1P5P/8 w - - 0 1",
        "best_move": "Bxc6",
        "id": "K.24",
        "evaluation_favours": WHITE
    },
    {
        "fen": "8/3nk3/3pp3/1B6/8/3PPP2/4K3/8 w - - 0 1",
        "best_move": "Bxd7",
        "id": "K.25",
        "evaluation_favours": WHITE
    },
]

BRATKO_KOPEC_TEST_SUITE = [
    {
        "fen": "1k1r4/pp1b1R2/3q2pp/4p3/2B5/4Q3/PPP2B2/2K5 b - - 0 1",
        "best_move": "Qd1+",
        "id": "BK.01",
        "evaluation_favours": BLACK 
    },
    {
        "fen": "3r1k2/4npp1/1ppr3p/p6P/P2PPPP1/1NR5/5K2/2R5 w - - 0 1",
        "best_move": "d5",
        "id": "BK.02",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "2q1rr1k/3bbnnp/p2p1pp1/2pPp3/PpP1P1P1/1P2BNNP/2BQ1PRK/7R b - - 0 1",
        "best_move": "f5",
        "id": "BK.03",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "rnbqkb1r/p3pppp/1p6/2ppP3/3N4/2P5/PPP1QPPP/R1B1KB1R w KQkq - 0 1",
        "best_move": "e6",
        "id": "BK.04",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "r1b2rk1/2q1b1pp/p2ppn2/1p6/3QP3/1BN1B3/PPP3PP/R4RK1 w - - 0 1",
        "best_move": "Nd5",
        "alternate_move": "a4",
        "id": "BK.05",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "2r3k1/pppR1pp1/4p3/4P1P1/5P2/1P4K1/P1P5/8 w - - 0 1",
        "best_move": "g6",
        "id": "BK.06",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "1nk1r1r1/pp2n1pp/4p3/q2pPp1N/b1pP1P2/B1P2R2/2P1B1PP/R2Q2K1 w - - 0 1",
        "best_move": "Nf6",
        "id": "BK.07",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "4b3/p3kp2/6p1/3pP2p/2pP1P2/4K1P1/P3N2P/8 w - - 0 1",
        "best_move": "f5",
        "id": "BK.08",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "2kr1bnr/pbpq4/2n1pp2/3p3p/3P1P1B/2N2N1Q/PPP3PP/2KR1B1R w - - 0 1",
        "best_move": "f5",
        "id": "BK.09",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "3rr1k1/pp3pp1/1qn2np1/8/3p4/PP1R1P2/2P1NQPP/R1B3K1 b - - 0 1",
        "best_move": "Ne5",
        "id": "BK.10",
        "evaluation_favours": BLACK 
    },
    {
        "fen": "2r1nrk1/p2q1ppp/bp1p4/n1pPp3/P1P1P3/2PBB1N1/4QPPP/R4RK1 w - - 0 1",
        "best_move": "f4",
        "id": "BK.11",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "r3r1k1/ppqb1ppp/8/4p1NQ/8/2P5/PP3PPP/R3R1K1 b - - 0 1",
        "best_move": "Bf5",
        "id": "BK.12",
        "evaluation_favours": BOTH 
    },
    {
        "fen": "r2q1rk1/4bppp/p2p4/2pP4/3pP3/3Q4/PP1B1PPP/R3R1K1 w - - 0 1",
        "best_move": "b4",
        "id": "BK.13",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "rnb2r1k/pp2p2p/2pp2p1/q2P1p2/8/1Pb2NP1/PB2PPBP/R2Q1RK1 w - - 0 1",
        "best_move": "Qd2",
        "alternate_move": "Qe1",
        "id": "BK.14",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "2r3k1/1p2q1pp/2b1pr2/p1pp4/6Q1/1P1PP1R1/P1PN2PP/5RK1 w - - 0 1",
        "best_move": "Qxg7+",
        "id": "BK.15",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "r1bqkb1r/4npp1/p1p4p/1p1pP1B1/8/1B6/PPPN1PPP/R2Q1RK1 w kq - 0 1",
        "best_move": "Ne4",
        "id": "BK.16",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "r2q1rk1/1ppnbppp/p2p1nb1/3Pp3/2P1P1P1/2N2N1P/PPB1QP2/R1B2RK1 b - - 0 1",
        "best_move": "h5",
        "id": "BK.17",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "r1bq1rk1/pp2ppbp/2np2p1/2n5/P3PP2/N1P2N2/1PB3PP/R1B1QRK1 b - - 0 1",
        "best_move": "Nb3",
        "id": "BK.18",
        "evaluation_favours": BOTH 
    },
    {
        "fen": "3rr3/2pq2pk/p2p1pnp/8/2QBPP2/1P6/P5PP/4RRK1 b - - 0 1",
        "best_move": "Rxe4",
        "id": "BK.19",
        "evaluation_favours": BLACK 
    },
    {
        "fen": "r4k2/pb2bp1r/1p1qp2p/3pNp2/3P1P2/2N3P1/PPP1Q2P/2KRR3 w - - 0 1",
        "best_move": "g4",
        "id": "BK.20",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "3rn2k/ppb2rpp/2ppqp2/5N2/2P1P3/1P5Q/PB3PPP/3RR1K1 w - - 0 1",
        "best_move": "Nh6",
        "id": "BK.21",
        "evaluation_favours": WHITE 
    },
    {
        "fen": "2r2rk1/1bqnbpp1/1p1ppn1p/pP6/N1P1P3/P2B1N1P/1B2QPP1/R2R2K1 b - - 0 1",
        "best_move": "Bxe4",
        "id": "BK.22",
        "evaluation_favours": BLACK 
    },
    {
        "fen": "r1bqk2r/pp2bppp/2p5/3pP3/P2Q1P2/2N1B3/1PP3PP/R4RK1 b kq - 0 1",
        "best_move": "f6",
        "id": "BK.23",
        "evaluation_favours": BLACK 
    },
    {
        "fen": "r2qnrnk/p2b2b1/1p1p2pp/2pPpp2/1PP1P3/PRNBB3/3QNPPP/5RK1 w - - 0 1",
        "best_move": "f4",
        "id": "BK.24",
        "evaluation_favours": WHITE 
    },
]
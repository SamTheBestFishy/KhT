field = 2

name1 = "../Output/trefoil_linked_with_line"
Tangle1 = Tangle("cup0.pos1.neg2.pos1.neg0.neg1.pos2.cap3.cap1")
BNcx1 = Tangle1.toReduced_BNComplex(1000, field)
multicurve1 = BNcx1.to_multicurve()
multicurve1.draw(name1+"_BNr","hdelta",Tangle1.slices)

name2 = "../Output/pseudo_trefoil_linked_with_line"
Tangle2 = Tangle("cup0.neg1.pos0.pos2.neg1.pos2.pos0.cap3.cap1")
BNcx2 = Tangle2.toReduced_BNComplex(1000, field)
multicurve2 = BNcx2.to_multicurve()
multicurve2.draw(name2+"_BNr","hdelta",Tangle2.slices)

name3 = "../Output/twist_linked_with_cap"
Tangle3 = Tangle("cup1.pos2.pos0.pos0.neg1.neg1.pos2.neg1.pos0.cap3.cap1")
BNcx3 = Tangle3.toReduced_BNComplex(1000, field)
multicurve3 = BNcx3.to_multicurve()
multicurve3.draw(name3+"_BNr","hdelta",Tangle3.slices)

name4 = "../Output/pretzel_3_minus_3_looped_bottom"
Tangle4 = Tangle("cup1.pos0.neg1.neg2.neg2.neg2.pos0.pos0.pos0.cap3.cap1")
BNcx4 = Tangle4.toReduced_BNComplex(1000, field)
multicurve4 = BNcx4.to_multicurve()
multicurve4.draw(name4+"_BNr","hdelta",Tangle4.slices)

name7 = "../Output/pretzel_2_minus_2_looped_bottom"
Tangle7 = Tangle("cup1.pos0.neg1.neg2.neg2.pos0.pos0.cap3.cap1")
BNcx7 = Tangle7.toReduced_BNComplex(1000, field)
multicurve7 = BNcx7.to_multicurve()
multicurve7.draw(name7+"_BNr","hdelta",Tangle7.slices)

name8 = "../Output/LiamsTangle"
Tangle8 = Tangle.LiamsTangle(1, [0])
BNcx8 = Tangle8.toReduced_BNComplex(1000, field)
multicurve8 = BNcx8.to_multicurve()
multicurve8.draw(name8+"_BNr","hdelta",Tangle8.slices)


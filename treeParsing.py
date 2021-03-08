# library import
import pandas as pd
import geopandas as gpd
import math

#!/usr/bin/env python

# Simpson Diversity Index
# http://en.wikipedia.org/wiki/Diversity_index

# modified from Shannon Diversity Index implementation by audy
# https://gist.github.com/audy/783125
# https://gist.github.com/audy

def simpson_di(keys, values):
	data = dict(zip(keys, values))
	""" Given a hash { 'species': count } , returns the Simpson Diversity Index
	
	>>> simpson_di({'a': 10, 'b': 20, 'c': 30,})
	0.3888888888888889
	"""

	def p(n, N):
		""" Relative abundance """
		if n is 0:
			return 0
		else:
			return float(n)/N

	N = sum(data.values())
	
	return 1-sum(p(n, N)**2 for n in data.values() if n is not 0)

def SimpsonEntropy(list):
	denom = sum(n*(n-1) for n in list if n != 0)
	numer = sum(list)*(sum(list)-1)
	return denom/numer

def ShannonEntropy(list):
	ent = 0.0
	for freq in list:
		try:
			ent = ent + freq * math.log(freq)
		except:
			pass
	ent = -ent
	return ent

def ShannonEntropyBlock(list):
	ListSum = sum(list)
	ent = 0.0
	for val in list:
		try:
			ent = ent + val/ListSum * math.log(val/ListSum)
		except:
			pass
	ent = -ent
	return ent

def speciesParse(cleanTrees, grid):
	treeMakeupNum = pd.DataFrame(cleanTrees[cleanTrees.within(grid.iloc[0].geometry)].groupby("Scientific").size()).T
	treeNum = treeMakeupNum.sum(axis=1)
	treeMakeup = pd.DataFrame(cleanTrees[cleanTrees.within(grid.iloc[0].geometry)].groupby("Scientific").sum()).T
	treeSum = treeMakeup.sum(axis=1)

	basalSimpson = simpson_di(list(treeMakeup.T.index), list(treeMakeup.T["BasalArea"]))
	stemSimpson = simpson_di(list(treeMakeupNum.T.index), list(treeMakeupNum.T[0]))

	for idx, column in enumerate(list(treeMakeup.columns)):
		treeMakeup[f"{column} sumPCT"] = treeMakeup.iloc[0][column]/treeSum
		treeMakeup[f"{column} numPCT"] = treeMakeupNum.iloc[0][column]/treeNum[0]

	treeMakeup['sum'] = treeSum
	treeMakeup['num'] = treeNum[0]
	treeMakeup['shannonDiversitySpeciesBasal'] = ShannonEntropy(list(treeMakeup[treeMakeup.filter(like='sumPCT').columns].values[0]))
	treeMakeup['simpsonDiversitySpeciesBasal'] = basalSimpson

	treeMakeup['shannonDiversitySpeciesStem'] = ShannonEntropy(list(treeMakeup[treeMakeup.filter(like='numPCT').columns].values[0]))
	treeMakeup['simpsonDiversitySpeciesStem'] = stemSimpson

	try:
		treeMakeup['mostAbundantPcSpeciesBasal'] = treeMakeup[treeMakeup.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		treeMakeup['mostAbundantNameSpeciesBasal'] = treeMakeup[treeMakeup.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["Scientific"][:-7]
		treeMakeup['mostAbundantPcSpeciesStem'] = treeMakeup[treeMakeup.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		treeMakeup['mostAbundantNameSpeciesStem'] = treeMakeup[treeMakeup.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["Scientific"][:-7]
	except: 
		print('error')

	treeMakeup.reset_index()

	tempDf = pd.DataFrame(cleanTrees[~cleanTrees.within(grid.iloc[0].geometry)].groupby("Scientific").sum()).T
	tempNum = pd.DataFrame(cleanTrees[~cleanTrees.within(grid.iloc[0].geometry)].groupby("Scientific").size()).T
	treeNum = tempNum.sum(axis=1)
	treeSum = tempDf.sum(axis=1)

	basalSimpson = simpson_di(list(tempDf.T.index), list(tempDf.T["BasalArea"]))
	stemSimpson = simpson_di(list(tempNum.T.index), list(tempNum.T[0]))

	for idx, column in enumerate(list(tempDf.columns)):
		tempDf[f"{column} sumPCT"] = tempDf.iloc[0][column]/treeSum
		tempDf[f"{column} numPCT"] = tempNum.iloc[0][column]/treeNum[0]

	tempDf['sum'] = treeSum
	tempDf['num'] = treeNum[0]
	tempDf['shannonDiversitySpeciesBasal'] = ShannonEntropy(list(tempDf[tempDf.filter(like='sumPCT').columns].values[0]))
	tempDf['simpsonDiversitySpeciesBasal'] = basalSimpson
	tempDf['shannonDiversitySpeciesStem'] = ShannonEntropy(list(tempDf[tempDf.filter(like='numPCT').columns].values[0]))
	tempDf['simpsonDiversitySpeciesStem'] = stemSimpson

	try:
		tempDf['mostAbundantPcSpeciesBasal'] = tempDf[tempDf.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		tempDf['mostAbundantNameSpeciesBasal'] = tempDf[tempDf.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["Scientific"][:-7]
		tempDf['mostAbundantPcSpeciesStem'] = tempDf[tempDf.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		tempDf['mostAbundantNameSpeciesStem'] = tempDf[tempDf.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["Scientific"][:-7]
	except: 
		print('error')

	treeMakeup = treeMakeup.append(tempDf)
	treeMakeup = treeMakeup.fillna(0).reset_index()
	
	return treeMakeup


def genusParse(cleanTrees, grid):
	treeMakeupNum = pd.DataFrame(cleanTrees[cleanTrees.within(grid.iloc[0].geometry)].groupby("CleanGenus").size()).T
	treeNum = treeMakeupNum.sum(axis=1)
	treeMakeup = pd.DataFrame(cleanTrees[cleanTrees.within(grid.iloc[0].geometry)].groupby("CleanGenus").sum()).T
	treeSum = treeMakeup.sum(axis=1)

	basalSimpson = simpson_di(list(treeMakeup.T.index), list(treeMakeup.T["BasalArea"]))
	stemSimpson = simpson_di(list(treeMakeupNum.T.index), list(treeMakeupNum.T[0]))

	for idx, column in enumerate(list(treeMakeup.columns)):
		treeMakeup[f"{column} sumPCT"] = treeMakeup.iloc[0][column]/treeSum
		treeMakeup[f"{column} numPCT"] = treeMakeupNum.iloc[0][column]/treeNum[0]

	treeMakeup['sum'] = treeSum
	treeMakeup['num'] = treeNum[0]
	treeMakeup['shannonDiversityGenusBasal'] = ShannonEntropy(list(treeMakeup[treeMakeup.filter(like='sumPCT').columns].values[0]))
	treeMakeup['simpsonDiversityGenusBasal'] = basalSimpson

	treeMakeup['shannonDiversityGenusStem'] = ShannonEntropy(list(treeMakeup[treeMakeup.filter(like='numPCT').columns].values[0]))
	treeMakeup['simpsonDiversityGenusStem'] = stemSimpson

	try:
		treeMakeup['mostAbundantPcGenusBasal'] = treeMakeup[treeMakeup.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		treeMakeup['mostAbundantNameGenusBasal'] = treeMakeup[treeMakeup.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["CleanGenus"][:-7]
		treeMakeup['mostAbundantPcGenusStem'] = treeMakeup[treeMakeup.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		treeMakeup['mostAbundantNameGenusStem'] = treeMakeup[treeMakeup.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["CleanGenus"][:-7]
	except: 
		print('error')

	treeMakeup.reset_index()


	tempDf = pd.DataFrame(cleanTrees[~cleanTrees.within(grid.iloc[0].geometry)].groupby("CleanGenus").sum()).T
	tempNum = pd.DataFrame(cleanTrees[~cleanTrees.within(grid.iloc[0].geometry)].groupby("CleanGenus").size()).T
	treeNum = tempNum.sum(axis=1)
	treeSum = tempDf.sum(axis=1)

	basalSimpson = simpson_di(list(tempDf.T.index), list(tempDf.T["BasalArea"]))
	stemSimpson = simpson_di(list(tempNum.T.index), list(tempNum.T[0]))

	for idx, column in enumerate(list(tempDf.columns)):
		tempDf[f"{column} sumPCT"] = tempDf.iloc[0][column]/treeSum
		tempDf[f"{column} numPCT"] = tempNum.iloc[0][column]/treeNum[0]

	tempDf['sum'] = treeSum
	tempDf['num'] = treeNum[0]
	tempDf['shannonDiversityGenusBasal'] = ShannonEntropy(list(tempDf[tempDf.filter(like='sumPCT').columns].values[0]))
	tempDf['simpsonDiversityGenusBasal'] = basalSimpson
	tempDf['shannonDiversityGenusStem'] = ShannonEntropy(list(tempDf[tempDf.filter(like='numPCT').columns].values[0]))
	tempDf['simpsonDiversityGenusStem'] = stemSimpson

	try:
		tempDf['mostAbundantPcGenusBasal'] = tempDf[tempDf.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		tempDf['mostAbundantNameGenusBasal'] = tempDf[tempDf.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["CleanGenus"][:-7]
		tempDf['mostAbundantPcGenusStem'] = tempDf[tempDf.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["CleanGenus"]
		tempDf['mostAbundantNameGenusStem'] = tempDf[tempDf.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["CleanGenus"][:-7]
	except: 
		print('error')
		
	treeMakeup = treeMakeup.append(tempDf)
	treeMakeup = treeMakeup.fillna(0).reset_index()

	return treeMakeup

def familyParse(cleanTrees, grid):
	treeMakeupNum = pd.DataFrame(cleanTrees[cleanTrees.within(grid.iloc[0].geometry)].groupby("family").size()).T
	treeNum = treeMakeupNum.sum(axis=1)
	treeMakeup = pd.DataFrame(cleanTrees[cleanTrees.within(grid.iloc[0].geometry)].groupby("family").sum()).T
	treeSum = treeMakeup.sum(axis=1)

	basalSimpson = simpson_di(list(treeMakeup.T.index), list(treeMakeup.T["BasalArea"]))
	stemSimpson = simpson_di(list(treeMakeupNum.T.index), list(treeMakeupNum.T[0]))

	for idx, column in enumerate(list(treeMakeup.columns)):
		treeMakeup[f"{column} sumPCT"] = treeMakeup.iloc[0][column]/treeSum
		treeMakeup[f"{column} numPCT"] = treeMakeupNum.iloc[0][column]/treeNum[0]

	treeMakeup['sum'] = treeSum
	treeMakeup['num'] = treeNum[0]
	treeMakeup['shannonDiversityFamilyBasal'] = ShannonEntropy(list(treeMakeup[treeMakeup.filter(like='sumPCT').columns].values[0]))
	treeMakeup['simpsonDiversityFamilyBasal'] = basalSimpson

	treeMakeup['shannonDiversityFamilyStem'] = ShannonEntropy(list(treeMakeup[treeMakeup.filter(like='numPCT').columns].values[0]))
	treeMakeup['simpsonDiversityFamilyStem'] = stemSimpson

	try:
		treeMakeup['mostAbundantPcFamilyBasal'] = treeMakeup[treeMakeup.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		treeMakeup['mostAbundantNameFamilyBasal'] = treeMakeup[treeMakeup.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["family"][:-7]
		treeMakeup['mostAbundantPcFamilyStem'] = treeMakeup[treeMakeup.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		treeMakeup['mostAbundantNameFamilyStem'] = treeMakeup[treeMakeup.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["family"][:-7]
	except: 
		print('error')
	
	treeMakeup.reset_index()

	tempDf = pd.DataFrame(cleanTrees[~cleanTrees.within(grid.iloc[0].geometry)].groupby("family").sum()).T
	tempNum = pd.DataFrame(cleanTrees[~cleanTrees.within(grid.iloc[0].geometry)].groupby("family").size()).T
	treeNum = tempNum.sum(axis=1)
	treeSum = tempDf.sum(axis=1)

	basalSimpson = simpson_di(list(tempDf.T.index), list(tempDf.T["BasalArea"]))
	stemSimpson = simpson_di(list(tempNum.T.index), list(tempNum.T[0]))

	for idx, column in enumerate(list(tempDf.columns)):
		tempDf[f"{column} sumPCT"] = tempDf.iloc[0][column]/treeSum
		tempDf[f"{column} numPCT"] = tempNum.iloc[0][column]/treeNum[0]

	tempDf['sum'] = treeSum
	tempDf['num'] = treeNum[0]
	tempDf['shannonDiversityFamilyBasal'] = ShannonEntropy(list(tempDf[tempDf.filter(like='sumPCT').columns].values[0]))
	tempDf['simpsonDiversityFamilyBasal'] = basalSimpson
	tempDf['shannonDiversityFamilyStem'] = ShannonEntropy(list(tempDf[tempDf.filter(like='numPCT').columns].values[0]))
	tempDf['simpsonDiversityFamilyStem'] = stemSimpson

	try:
		tempDf['mostAbundantPcFamilyBasal'] = tempDf[tempDf.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		tempDf['mostAbundantNameFamilyBasal'] = tempDf[tempDf.filter(like='sumPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["family"][:-7]
		tempDf['mostAbundantPcFamilyStem'] = tempDf[tempDf.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["BasalArea"]
		tempDf['mostAbundantNameFamilyStem'] = tempDf[tempDf.filter(like='numPCT').columns].T.sort_values("BasalArea", ascending=False).reset_index().iloc[0]["family"][:-7]
	except: 
		print('error')
		
	treeMakeup = treeMakeup.append(tempDf)
	treeMakeup = treeMakeup.fillna(0).reset_index()

	return treeMakeup
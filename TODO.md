```c
void processScore(){
	getScore(MathScore, EngScore, PhyScore, ArtScore, MusicSore);
	
	ccalculateSumAverage(s_ID, MathScore, EngScore, PhyScore, ArtScore, MusicScore);
	print(S_ID, total, average)
}

void calculateSumAverage(double s_ID, int MathScore, int EngScore, int PhyScore, int ArtScore, int MusicScore){
	total = calculateSum(MathScore,EngScore,PhyScore, ArtScore, MusicScore);
	average = total / count(score);
}
```

```
typedef struct Score{

};
```
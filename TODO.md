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
typedef struct Score {  
    int MathScore;  
    int EngScore;  
    int PhyScore;  
    int ArtScore;  
    int MusicScore;  
} Score;  
  
void processScore(){  
    Score score;  
    getScore(score);  
  
    int total = calculateSum(score);  
    double average = ccalculateSumAverage(Score);  
    print(S_ID, total, average);  
}  
  
double calculateSumAverage(Score score){  
    int total = calculateSum(score);  
    double average = total / count(score);  
  
    return average;  
}
};
```


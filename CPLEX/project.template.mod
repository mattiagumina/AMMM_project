// ** PLEASE ONLY CHANGE THIS FILE WHERE INDICATED **
// In particular, do not change the names of the variables.

int                    D = ...;
int              n[1..D] = ...;
int                    N = ...;
int              d[1..N] = ...;
float      m[1..N][1..N] = ...;


// Define here your decision variables and
// any other auxiliary program variables you need.
// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>
range members = 1..N;
range departments = 1..D;

dvar boolean x[i in members];

int nMembersInCommission = sum(p in departments) n[p];

execute {
    cplex.tilim = 1800;
}
//<<<<<<<<<<<<<<<<

// Write here the objective function.

//>>>>>>>>>>>>>>>>
maximize (sum(i in members) x[i] * sum(j in i+1..N) x[j] * m[i][j]) / (nMembersInCommission * (nMembersInCommission - 1) / 2);
//<<<<<<<<<<<<<<<<



subject to {

    // Write here the constraints.

    //>>>>>>>>>>>>>>>>
        
	// Constraint 1
	forall(p in departments)
	  sum(i in members: d[i] == p) x[i] == n[p];
	  
	// Constraint 2
	forall(i in members)
	  forall(j in i+1..N: m[i][j] == 0.00)
	    x[i] + x[j] <= 1;
	
	// Constraint 3
	forall(i in members)
	  	forall(j in i+1..N: m[i][j] > 0.00 && m[i][j] < 0.15)
	    	sum(k in members: m[i][k] > 0.85 && m[j][k] > 0.85) x[k] >= x[i] + x[j] - 1;
    //<<<<<<<<<<<<<<<<
}

// You can run an execute block if needed.

//>>>>>>>>>>>>>>>>
execute{
	write("\nCommission: ")
	for(var i = 1; i <= N; i++){
	  if(x[i] == 1){
	    write(i + " ");
	  }
	}
}
//<<<<<<<<<<<<<<<<

import handtracking

vertical_division=float(1.0/2.0)  #represent 0.5ths of the screen (vertically divided) 1/3 is 1/3rd on the left hand and 2/3rds on the ri
threshold = 60 #no change needed in most situations

handtracking.findHandPos_standalone(vertical_division, threshold)
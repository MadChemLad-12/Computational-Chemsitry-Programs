function datefiles() { 
    echo "attempting to date files as $(date +%d-%m-%Y)"

    if [ -f E.txt ]
    then
        mv E.txt E_$(date +%d-%m-%Y).txt
    else
        echo "there is no E.txt file"   
    fi

    if [ -f OSZICAR ]
    then
        mv OSZICAR OSZICAR_$(date +%d-%m-%Y)
    else
        echo "there is no OSZICAR file"   
    fi


        if [ -f OUTCAR ]
    then
        mv OUTCAR OUTCAR_$(date +%d-%m-%Y)
    else
        echo "there is no OUTCAR file"   
    fi


        if [ -f vasp.log  ]
    then
        mv vasp.log vasp.log_$(date +%d-%m-%Y).log
    else
        echo "there is no vasp.log file"   
    fi


        if [ -f XDATCAR ]
    then
        mv XDATCAR XDATCAR_$(date +%d-%m-%Y)
    else
        echo "there is no XDATCAR file"   
    fi


} 

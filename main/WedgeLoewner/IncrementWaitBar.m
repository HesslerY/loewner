function IncrementWaitBar(wb,inner_points)
    ud = wb.UserData;
    ud(1) = ud(1) + 1;
    ud(2) = ud(2) + ud(1)*inner_points;
    waitbar(ud(2) / ud(3), wb, ud(2));
    wb.UserData = ud;
end

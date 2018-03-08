function r = FindAngle(z_sol1,z_sol2)

    z1 = z_sol1(end)
    z2 = z_sol2(end)

    angle1 = atan2(imag(z1),real(z1))
    angle2 = atan2(imag(z2),real(z2))

    r = abs(angle1 - angle2)
end

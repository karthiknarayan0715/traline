# r = -1
# if r==-1:
#     return redirect(url_for('shortline_symmetrical'))
# #Results
# ind_per_ph = result['Inductance per Phase'] = f"{2*10**(-4)*(math.log(d/(0.7784*r)))} H/km"
# cam_per_ph = result['Capacitance per Phase'] = f"{str(0)} F/km"
# ind_reac = result['Inductive Reactance'] = f"{float(ind_per_ph[0:-5])*frequency} ohms/km"
# cap_reac = result['Capacitance Reactance'] = f"Infinity ohms"
# A_parameter = result['A Parameter'] = f"{1}"
# B_parameter = result['B Parameter'] = f"{ind_per_ph[0:-5]}"
# C_parameter = result['C Parameter'] = f"{0}"
# D_parameter = result['D Parameter'] = f"{1}"
# sending_end_vol = result['Sending End Voltage'] = f"{voltage_line+(I*(resistance_per_km+ind_per_ph)*l)/1000} V"
# sending_end_cur = result['Sending End Current'] = f"{I} A"
# voltage_regulation = result['Voltage Regulation'] = f"{(voltage_line - sending_end_vol)/sending_end_vol}"
# power_loss = result['Power Loss'] = f"{(I**2)*resistance_per_km*l}"


    # #form inputs
# spacing = float(form.get('spacing'))
# n_s_c = float(form.get('sub-cond'))
# d = float(form.get('sub_space'))
# d_strand = float(form.get('strand_dia'))
# l = float(form.get('length'))
# resistance_per_km = float(form.get('resistance'))
# frequency = float(form.get('frequency'))
# voltage_line = float(form.get('voltage'))
# load_3_ph = float(form.get('load'))
# pf = float(form.get('pf'))
# load_mva = load_3_ph/(3*pf)   
# I = load_mva/(voltage_line/(3**0.5))
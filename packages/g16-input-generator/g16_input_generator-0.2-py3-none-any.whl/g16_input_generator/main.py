import tkinter as tk
from tkinter import ttk, filedialog
from rdkit import Chem
from rdkit.Chem import AllChem


def smiles_to_xyz(smiles_string):
    mol = Chem.MolFromSmiles(smiles_string)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol, AllChem.ETKDG())
    AllChem.MMFFOptimizeMolecule(mol)

    xyz_str = ""
    for atom in mol.GetAtoms():
        pos = mol.GetConformer().GetAtomPosition(atom.GetIdx())
        xyz_str += "{}\t{}\t{}\t{}\n".format(atom.GetSymbol(), pos.x, pos.y, pos.z)

    return xyz_str


def generate_gaussian_input(smiles_string, gaussian_params, computation_params, chk_filename):
    xyz_data = smiles_to_xyz(smiles_string)

    input_string = f"%chk={chk_filename}\n"
    input_string += f"%mem={gaussian_params['memory']}\n"
    input_string += f"%nproc={gaussian_params['nproc']}\n"
    
    scrf_string = ""
    if computation_params['solvent'] and computation_params['solvent_method']:
        scrf_string = f"scrf=({computation_params['solvent_method']},solvent={computation_params['solvent']})"

    input_string += f"# {computation_params['method']} {computation_params['theory']}/{computation_params['basis']} {'symmetry=centerofmass'} {scrf_string} {computation_params['other']}\n\n"
    input_string += f"{name_var.get()}_{computation_params['theory']}_{computation_params['basis']}_{computation_params['method']}\n\n"
    input_string += computation_params['charge_and_multiplicity'] + "\n"
    input_string += xyz_data + "\n"

    return input_string

def generate_and_save():

  # Check if molecule name or SMILES string is empty
    if not name_var.get().strip():
        result_label.config(text="Error - molecule name required")
        return
    elif not smiles_var.get().strip():
        result_label.config(text="Error - SMILES string required")
        return

    gaussian_params = {
        'memory': memory_var.get(),
        'nproc': nproc_var.get()
    }

    computation_params = {
        'theory': theory_var.get(),
        'basis': basis_var.get(),
        'method': method_var.get(),
        'solvent': solvent_var.get(),
        'solvent_method': solvent_method_var.get(),
        'other' : other_var.get(),
        'charge_and_multiplicity': charge_multiplicity_var.get()
    }

     # Check if either solvent or solvent method is specified, but not both
    if (computation_params['solvent'] and not computation_params['solvent_method']) or (not computation_params['solvent'] and computation_params['solvent_method']):
        result_label.config(text="Error - Both solvent and solvent method are required")
        return

    smiles_string = smiles_var.get()

    method_str = method_var.get()
    if method_str == "opt":
        method_str = 'gs'
    if method_str == "opt=tight":
        method_str = 'gs'
    if method_str == "td=(root=1,nstates=30,noneqsolv)":
        method_str = 'es'
    
    solvent_str = solvent_var.get()
    if solvent_str == '':
        solvent_str = 'vac'
    

    default_filename = f"{name_var.get()}_{method_str}_{theory_var.get()}_{basis_var.get()}_{solvent_str}{solvent_method_var.get()}.gjf"
    chk_filename = default_filename.replace(".gjf", ".chk")
    
    gaussian_input = generate_gaussian_input(smiles_string, gaussian_params, computation_params, chk_filename)
    
    file_path = filedialog.asksaveasfilename(defaultextension=".gjf", initialfile=default_filename, filetypes=[("Gaussian Input Files", "*.gjf"), ("All Files", "*.*")])
    
    if file_path:
        with open(file_path, "w") as f:
            f.write(gaussian_input)

        result_label.config(text=f"File saved to {file_path}")
    else:
        result_label.config(text="File save cancelled.")

# Create the main window
root = tk.Tk()
root.title("g16 Input Generator")

# Variables to hold user input
name_var = tk.StringVar()
smiles_var = tk.StringVar()
memory_var = tk.StringVar(value="30GB")
nproc_var = tk.StringVar(value="48")
theory_var = tk.StringVar(value="M06-2X")
basis_var = tk.StringVar(value="6-31G(d)")
method_var = tk.StringVar(value="opt")
solvent_var = tk.StringVar()
solvent_method_var = tk.StringVar()
other_var = tk.StringVar()
charge_multiplicity_var = tk.StringVar(value="0 1")
THEORIES = [
    "M06-2X", "CAM-B3LYP", "B3LYP", "HF"]

BASIS_SETS = [
    "6-31G(d,p)", "LanL2MB","LanL2DZ", "6-31G", "6-31G(d)", "6-311G", "6-311++G(3df,3pd)", "cc-pVDZ", "cc-pVTZ"
]

METHODS = [
    'opt', 'opt=tight','td=(root=1,nstates=30,noneqsolv)'
]

SOLVENTS = ['water' , 'n-octanol', 'dichloromethane']

SOLVENT_METHODS = ['PCM', 'SMD']

# Create and place the widgets
ttk.Label(root, text="Enter Molecule Name:").grid(row=0, column=0, sticky="w", padx=5, pady=5)  
ttk.Entry(root, textvariable=name_var).grid(row=0, column=1, sticky="ew", padx=5, pady=5)

ttk.Label(root, text="Enter SMILES:").grid(row=1, column=0, sticky="w", padx=5, pady=5) 
ttk.Entry(root, textvariable=smiles_var).grid(row=1, column=1, sticky="ew", padx=5, pady=5)

ttk.Label(root, text="Memory:").grid(row=2, column=0, sticky="w", padx=5, pady=5)  
ttk.Entry(root, textvariable=memory_var).grid(row=2, column=1, sticky="ew", padx=5, pady=5)

ttk.Label(root, text="nproc:").grid(row=3, column=0, sticky="w", padx=5, pady=5)  
ttk.Entry(root, textvariable=nproc_var).grid(row=3, column=1, sticky="ew", padx=5, pady=5)

ttk.Label(root, text="Method:").grid(row=4, column=0, sticky="w", padx=5, pady=5)  
theory_combobox = ttk.Combobox(root, values=METHODS, textvariable=method_var)
theory_combobox.grid(row=4, column=1, sticky="ew", padx=5, pady=5)
theory_combobox.set("opt")  # Default value

ttk.Label(root, text="Solvent:").grid(row=5, column=0, sticky="w", padx=5, pady=5)  
solvent_combobox = ttk.Combobox(root, values=SOLVENTS, textvariable=solvent_var)
solvent_combobox.grid(row=5, column=1, sticky="ew", padx=5, pady=5)
solvent_combobox.set('')

ttk.Label(root, text="Solvent Method:").grid(row=6, column=0, sticky="w", padx=5, pady=5)  
solvent_method_combobox = ttk.Combobox(root, values=SOLVENT_METHODS, textvariable=solvent_method_var)
solvent_method_combobox.grid(row=6, column=1, sticky="ew", padx=5, pady=5)
solvent_method_combobox.set('')  

ttk.Label(root, text="Theory:").grid(row=7, column=0, sticky="w", padx=5, pady=5)  
theory_combobox = ttk.Combobox(root, values=THEORIES, textvariable=theory_var)
theory_combobox.grid(row=7, column=1, sticky="ew", padx=5, pady=5)
theory_combobox.set("M06-2X")  # Default value

ttk.Label(root, text="Basis:").grid(row=8, column=0, sticky="w", padx=5, pady=5)  
basis_combobox = ttk.Combobox(root, values=BASIS_SETS, textvariable=basis_var)
basis_combobox.grid(row=8, column=1, sticky="ew", padx=5, pady=5)
basis_combobox.set("6-31G(d,p)")  # Default value

ttk.Label(root, text="Other:").grid(row=9, column=0, sticky="w", padx=5, pady=5)  
ttk.Entry(root, textvariable=other_var).grid(row=9, column=1, sticky="ew", padx=5, pady=5)

ttk.Label(root, text="Charge & Multiplicity:").grid(row=10, column=0, sticky="w", padx=5, pady=5)  
ttk.Entry(root, textvariable=charge_multiplicity_var).grid(row=10, column=1, sticky="ew", padx=5, pady=5)

ttk.Button(root, text="Generate & Save Input File", command=generate_and_save).grid(row=11, column=0, columnspan=2, pady=10)  

result_label = ttk.Label(root, text="", wraplength=580)
result_label.grid(row=12, column=0, columnspan=2, pady=5, sticky="ew") 

root.columnconfigure(1, weight=1)  # Make the second column expandable
root.geometry('600x450')
root.mainloop()


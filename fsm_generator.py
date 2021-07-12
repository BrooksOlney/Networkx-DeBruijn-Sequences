from debruijn import DeBruijnGraph

n = 16
dbgraph = DeBruijnGraph(n)
seqs = dbgraph.gen_multiple_sequences(1)

def write_verilog_de_bruijn(seq, n):

    seqs = [seq[i:i+n] for i in range(len(seq) - n + 1)] + [seq[:n]]

    vlog = []

    vlog.append(f'module db2_{n}(input rst, input clk, output [{n-1}:0] db_out);')
    vlog.append(f'\treg [{n-1}:0] current_state, next_state;')
    vlog.append(f'\tassign db_out = current_state;')
    vlog.append(f'\talways @ (negedge clk) begin')
    vlog.append(f'\t\tif (rst) begin')
    vlog.append(f'\t\t\tcurrent_state <= {n}\'b{seqs[0]};')
    vlog.append(f'\t\tend')
    vlog.append(f'\t\telse begin')
    vlog.append(f'\t\t\tcurrent_state <= next_state;')
    vlog.append(f'\t\tend')
    vlog.append(f'\tend')

    vlog.append(f'\talways @ (posedge clk) begin')
    vlog.append(f'\t\tcase(current_state)')
    
    for i, state in enumerate(seqs[:-1]):
        vlog.append(f'\t\t\t{n}\'b{state}\t:\tnext_state <= {n}\'b{seqs[i+1]};')
    
    vlog.append(f'\t\tendcase')
    vlog.append(f'\tend')
    vlog.append(f'endmodule')

    with open(f'F:\\Research\\Networkx-DeBruijn-Sequences\\db2_{n}.v', 'w') as vfile:
        vfile.write('\n'.join(vlog))

write_verilog_de_bruijn(seqs[0], n)
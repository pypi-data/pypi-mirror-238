


class params:
	def __init__ (this, struct, level):
		this.struct = struct
		this.level = level
		
		
struct = {
	"name": "this name"
}
p = params (struct, 0)

p.struct["name 2"] = "another name"

print (struct)
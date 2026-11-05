from pathlib import Path

p = Path("m4/ax_boost_system.m4")
s = p.read_text()

old = """            if test "x$ax_lib" = "x"; then
                AC_MSG_ERROR(Could not find a version of the Boost::System library!)
            fi
"""

new = """            if test "x$ax_lib" = "x"; then
                dnl Modern Boost.System is header-only (Boost >= 1.69).
                BOOST_SYSTEM_LIB=""
                AC_SUBST(BOOST_SYSTEM_LIB)
                AC_MSG_NOTICE([Using header-only Boost.System])
            fi
"""

if old not in s:
    raise SystemExit("ERROR: Original code not found; no changes made.")

p.write_text(s.replace(old, new, 1))
print("Patched:", p)

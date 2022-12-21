# -*- coding: utf-8 -*-
"""
Created on Mon Dec 19 15:03:46 2022

@author: 500585
"""

import streamlit as st

st.set_page_config(
    page_title="elastomech",
    page_icon="🛠",
    layout='wide')

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True


if check_password():
        
    tab1, tab2 = st.tabs(["English", "Deutsch"])
    
    with tab1:

        st.markdown(
            """
            # elastomech.py 🛠
            
            ## Support forces and working radius using a substitute model 
            
            ### Resources
            - [Theoretical background](https://github.com/l-mech/elastomech/blob/main/resources/Elastostatic%20model%20for%20platform%20supports%20Rev%20A.pdf)
            - [Github Repo](https://github.com/l-mech/elastomech)
            
            ### How to use
            **👈 Select a page from the sidebar** to enter calculations
            
            **Make sure to use a consistent unit system!** The script does not know about units, you can choose the unit system as you like, but everything has to fit together.
            
            Useful consistent unit systems are:
            - ``SI system: m, kg, N``
            - ``mm-t-s: (mm, t, N)``
            - ``mm-kg-ms: (mm, kg, kN)``
            
            #### Support Force Distribution Tool
            Using the **Support Force Distribution** tool the support forces and other values can be determined for a specific load condition.
            
            To do this, specify all the required parameters in the sidebar, the diagrams update continuously.
                    
            The results include the following quantities:
            - ``f1...f4``: Support forces of the four supports
            - ``t14x, t23x``: Torques induced in the two virtual torsion springs of the frame
            - ``s1...s4``: Deflection of the four supports. Negative values mean that one support lifts off.
            - ``f12...f14``: Residual loads of the four tilt edges, where the residual load is the sum of two neighboring support forces
            
            When a support lifts off, the calculation in the background switches from the statically overdetermined model (four feet on the floor) to the statically determined model (three feet on the floor).
            
            Mathematically, the corresponding support force is set to $$F_i=0$$ and the spring equation ($$F_i=s_i\cdot D_i$$) of the respective support is removed from the equation system.
            
            #### Working Radius Tool
            With the **Working Radius** tool we can create a working range limit curve that is limited by different boundaries.
            
            These boundaries include:
            - Working radius ``ro`` itself (e.g. limited by boom length)
            - Residual load ``rl`` (with ``rl = min(f12, f23, f34, f14)``)
            - Support forces ``f1...f4``
            - Torsional moments ``t14x``, ``t23x`` in the virtual torsion springs of the frame
            For each of the quantities a lower bound and an upper bound can be defined.
            
            For each step $$0°\leq \phi_i \leq 360°$$ the script tries to maximize the working radius ``ro`` within the given bounds using the ``SLSQP`` method ([Sequential Least Squares Programming](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp)).
            If no solution can be found the algorithm stops after a defined number of iterations.
    
            The actual load moment ``ml`` as input for the calculation is calculated as $$M_L = r_o \cdot F_{ro}$$. This means that only one load on the boom is considered, namely the force at the tip of the boom ``f_ro``. No dead weight of the boom or other additional forces are included in this calculation, because the position of these forces cannot be determined with certainty as a function of the working radius ``ro`` (the same outreach can be achieved with different positions of the boom).                                                                                                                      
            
            **Please be aware that it's easily possible to set the constraints in such a way that there are no more admissible solutions.** In this case the script skips the calculation and steps to next angle $$\phi_i$$ (an error log is shown after the loop finishes).
            However, the calculation can take very long in this case, because the optimization algorithm tries to determine a solution until the maximum allowed iterations are reached. Check the diagrams next to the polar plot to get an idea of which boundaries might cause problems.
            
            After setting all parameters, the calculation is started with the button.
            
            Results and input values can be downloaded as csv files using the corresponding download buttons.
        """
        )
                                                                                                                                                                 
    with tab2:
        
        st.markdown(
            """
            # elastomech.py 🛠
            
            ## Stützkräfte und Arbeitsradius via Ersatzmodell
            
            ### Ressourcen
            - [Theoretischer Hintergrund](https://github.com/l-mech/elastomech/blob/main/resources/Elastostatic%20model%20for%20platform%20supports%20Rev%20A.pdf)
            - [Github Repo](https://github.com/l-mech/elastomech)
            
            ### Hinweise zur Anwendung
            **👈 Wähle eine Seite in der Seitenleiste**, um zu starten
            
            **Stelle sicher, dass du ein konsistentes Einheitensystem verwendest!** Das Skript kennt keine Einheiten, du kannst das Einheitensystem frei wählen, aber alles muss zusammenpassen.
            
            Nützliche konsistente Einheitensysteme sind:
            - ``SI-System: m, kg, N``
            - ``mm-t-s: (mm, t, N)``
            - ``mm-kg-ms: (mm, kg, kN)``
            
            #### Stützkraftverteilung
            Mit dem Tool **Support Force Distribution** können die Stützenkräfte und andere Werte für einen bestimmten Lastfall ermittelt werden.
            
            Gib dazu alle erforderlichen Parameter in der Seitenleiste an, die Diagramme werden laufend aktualisiert.
                    
            Die Ergebnisse umfassen die folgenden Größen:
            - ``f1...f4``: Stützenkräfte der vier Auflager
            - ``t14x, t23x``: In den beiden virtuellen Torsionsfedern des Rahmens induzierte Drehmomente
            - ``s1...s4``: Federwege der vier Stützen. Negative Werte bedeuten, dass eine Stütze abhebt.
            - ``f12...f14``: Restlasten der vier Kippkanten, wobei die Restlast die Summe von zwei benachbarten Stützenkräften ist
            
            Wenn eine Stütze abhebt, wechselt die Berechnung im Hintergrund von dem statisch überbestimmten Modell (vier Füße auf dem Boden) zu dem statisch bestimmten Modell (drei Füße auf dem Boden).
            
            Mathematisch wird die entsprechende Stützenkraft auf $$F_i=0$$ gesetzt und die Federgleichung ($$F_i=s_i\cdot D_i$$) der jeweiligen Stütze aus dem Gleichungssystem entfernt.
            
            #### Ausladungskurve
            Mit dem Tool **Working Radius** können wir eine Grenzkurve für den Arbeitsbereich erstellen, die durch verschiedene Grenzen eingeschränkt ist.
            
            Diese Grenzen umfassen:
            - Ausladung (Arbeitsradius) ``ro`` selbst (z.B. begrenzt durch Auslegerlänge)
            - Restlast ``rl`` (mit ``rl = min(f12, f23, f34, f14)``)
            - Stützkräfte ``f1...f4``
            - Torsionsmomente ``t14x``, ``t23x`` in den virtuellen Torsionsfedern des Rahmens
            Für jede der Größen kann eine untere und eine obere Schranke definiert werden.
            
            Für jeden Schritt $$0°\leq \phi_i \leq 360°$$ versucht das Skript, den Arbeitsradius ``ro`` innerhalb der vorgegebenen Schranken mit Hilfe der Methode ``SLSQP`` ([Sequential Least Squares Programming](https://docs.scipy.org/doc/scipy/reference/optimize.minimize-slsqp.html#optimize-minimize-slsqp)) zu maximieren.
            Wenn keine Lösung gefunden werden kann, bricht der Algorithmus nach einer bestimmten Anzahl von Iterationen ab.
    
            Das tatsächliche Lastmoment ``ml`` als Eingabe für die Berechnung wird berechnet als $$M_L = r_o \cdot F_{ro}$$. Das bedeutet, dass nur eine einzige Last auf den Ausleger berücksichtigt wird, nämlich die Kraft an der Spitze des Auslegers ``f_ro``. Das Eigengewicht des Auslegers oder andere Zusatzkräfte werden in dieser Berechnung nicht berücksichtigt, da die Lage dieser Kräfte in Abhängigkeit vom Arbeitsradius ``ro`` nicht sicher bestimmt werden kann (die gleiche Ausladung kann mit unterschiedlichen Positionen des Auslegers erreicht werden).                                                                                                                      
            
            **In diesem Fall überspringt das Skript die Berechnung und geht zum nächsten Winkel $$\phi_i$$ über (ein Fehlerprotokoll wird nach Beendigung der Schleife angezeigt).
            Allerdings kann die Berechnung in diesem Fall sehr lange dauern, da der Optimierungsalgorithmus versucht, eine Lösung zu ermitteln, bis die maximal zulässigen Iterationen erreicht sind. Sie in die Diagramme neben dem Polardiagramm, um eine Vorstellung davon zu bekommen, welche Grenzen Probleme verursachen könnten.
            
            Nachdem alle Parameter eingestellt sind, wird die Berechnung über den entsprechenden Button gestartet.
            
            Die Ergebnisse und Eingabewerte können über die entsprechenden Download-Buttons als csv-Dateien heruntergeladen werden.
        """
        )                                                                                                                                                          
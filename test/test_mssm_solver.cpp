#include "mssm_solver.h"
#include "mssm_two_scale.hpp"
#include "mssm_two_scale_initial_guesser.hpp"
#include "mssm_two_scale_sugra_constraint.hpp"
#include "mssm_two_scale_convergence_tester.hpp"
#include "softsusy.h"
#include "two_scale_solver.hpp"
#include "logger.hpp"

#define BOOST_TEST_DYN_LINK
#define BOOST_TEST_MODULE test_mssm_solver

#include <boost/test/unit_test.hpp>

BOOST_AUTO_TEST_CASE( test_softsusy_mssm_solver )
{
   DoubleVector highScaleSoftPars(3);
   const double m12 = 500., a0 = 0., m0 = 125.;
   highScaleSoftPars(1) = m0;
   highScaleSoftPars(2) = m12;
   highScaleSoftPars(3) = a0;

   const int signMu = 1;
   const double tanBeta = 10.0;
   const bool uni = true;
   const double mxGuess = 1.0e16;

   QedQcd oneset;
   const double alphasMZ = 0.1187, mtop = 173.4, mbmb = 4.2;
   oneset.setAlpha(ALPHAS, alphasMZ);
   oneset.setPoleMt(mtop);
   oneset.setMass(mBottom, mbmb);
   oneset.toMz();

   RGFlow<SoftSusy_t> mssmSolver;
   mssmSolver.setSoftHighScalePars(highScaleSoftPars);
   mssmSolver.setSignMu(signMu);
   mssmSolver.setTanBeta(tanBeta);
   mssmSolver.setLowScaleBoundaryConditions(oneset);
   mssmSolver.setGaugeUnification(uni);
   mssmSolver.setMxGuess(mxGuess);
   mssmSolver.setHighScaleBoundaryCondition(sugraBcs);
   mssmSolver.solve();

   MssmSoftsusy softSusy;
   softSusy.lowOrg(sugraBcs, mxGuess, highScaleSoftPars, signMu, tanBeta, oneset, uni);

   BOOST_CHECK_EQUAL(mssmSolver.displayPhys(), softSusy.displayPhys());
}

class Mssm_low_energy_constraint : public Constraint<Two_scale> {
public:
   Mssm_low_energy_constraint(Mssm<Two_scale>* mssm_, const QedQcd& oneset_,
                              double tanBeta_, double scale_)
      : mssm(mssm_)
      , oneset(oneset_)
      , tanBeta(tanBeta_)
      , scale(scale_)
      {}
   virtual ~Mssm_low_energy_constraint() {}
   virtual void apply() {
      mssm->calcDrBarPars();
   }
   virtual double get_scale() const { return scale; }
   virtual void update_scale() {
      drBarPars tree(mssm->displayDrBarPars());
      double tmp_scale = sqrt(tree.mu(2, 3) * tree.mu(1, 3));
      if (tmp_scale > 0.0)
         scale = tmp_scale;
   }

private:
   Mssm<Two_scale>* mssm;
   QedQcd oneset;
   double tanBeta;
   double scale;
};

BOOST_AUTO_TEST_CASE( test_softsusy_mssm_with_generic_rge_solver )
{
   DoubleVector highScaleSoftPars(3);
   const double m12 = 500., a0 = 0., m0 = 125.;
   highScaleSoftPars(1) = m0;
   highScaleSoftPars(2) = m12;
   highScaleSoftPars(3) = a0;

   const int signMu = 1;
   const double tanBeta = 10.0;
   const bool uni = true;
   const double mxGuess = 1.0e16;

   QedQcd oneset;
   const double alphasMZ = 0.1187, mtop = 173.4, mbmb = 4.2;
   oneset.setAlpha(ALPHAS, alphasMZ);
   oneset.setPoleMt(mtop);
   oneset.setMass(mBottom, mbmb);
   oneset.toMz();

   Mssm<Two_scale> mssm;
   mssm.setScale(125);
   mssm.setSusyMu(signMu * 1.0);
   mssm.setTanb(tanBeta);
   mssm.setData(oneset);

   Mssm_sugra_constraint mssm_sugra_constraint(&mssm, mxGuess, m0, m12, a0, signMu);
   Mssm_low_energy_constraint mssm_low_energy_constraint(&mssm, oneset, tanBeta, m0);
   Mssm_convergence_tester mssm_convergence_tester(&mssm, 0.1);
   Mssm_initial_guesser initial_guesser(&mssm, oneset, mxGuess, tanBeta, signMu, highScaleSoftPars, false);

   std::vector<Constraint<Two_scale>*> mssm_constraints;
   mssm_constraints.push_back(&mssm_low_energy_constraint);
   mssm_constraints.push_back(&mssm_sugra_constraint);

   RGFlow<Two_scale> solver;
   solver.set_max_iterations(10);
   solver.set_convergence_tester(&mssm_convergence_tester);
   solver.set_initial_guesser(&initial_guesser);
   solver.add_model(&mssm, mssm_constraints);
   try {
      solver.solve();
   } catch (RGFlow<Two_scale>::Error& e) {
      BOOST_ERROR(e.what());
   }

   MssmSoftsusy softSusy;
   softSusy.lowOrg(sugraBcs, mxGuess, highScaleSoftPars, signMu, tanBeta, oneset, uni);

   BOOST_CHECK_EQUAL(mssm.displayPhys(), softSusy.displayPhys());
}

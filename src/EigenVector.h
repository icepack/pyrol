#include <Eigen/Core>
#include <ROL_Vector.hpp>

#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
namespace py = pybind11;

class EigenVector : public ROL::Vector<double>
{
	private:
		std::shared_ptr<Eigen::VectorXd> _vec;
	public:
		EigenVector(int size)
		{
			_vec = std::make_shared<Eigen::VectorXd>(size);
		}

		EigenVector(py::array_t<double> a)
		{
			auto buf = a.request();
			if(buf.ndim != 1)
				throw std::runtime_error("Dimension of numpy array must be one.");
			Eigen::Map<Eigen::VectorXd> m(static_cast<double *>(buf.ptr), buf.shape[0]);
			_vec = std::make_shared<Eigen::VectorXd>(m);
		}

		EigenVector(std::shared_ptr<Eigen::VectorXd> vec)
		{
			_vec = vec;
		}

		virtual void plus(const ROL::Vector<double>& x)
		{
			//  std::cout << "plus-" << xx._vec->str(false) << " ";
			const EigenVector& xx = Teuchos::dyn_cast<const EigenVector>(x);
			*_vec += *(xx._vec);
			//*_vec += *(xx._vec);
		}

		virtual void scale(const double alpha)
		{
			// std::cout << "scale-";
			*_vec *= alpha; 
		}

		virtual double dot(const ROL::Vector<double> &x) const
		{
			//       std::cout << "dot-";
			const EigenVector& xx = Teuchos::dyn_cast<const EigenVector>(x);
			return _vec->dot(*(xx._vec));
		}
		/// Return L2 norm of ROLVector
		virtual double norm() const
		{
			//      std::cout << "norm\n";
			return _vec->norm();
		}

		virtual int dimension() const {
			return _vec->size();
		}

		virtual Teuchos::RCP<ROL::Vector<double>> clone() const
		{
			//      std::cout << "clone\n";
			auto new_vec = Teuchos::rcp(new EigenVector(std::make_shared<Eigen::VectorXd>(*_vec)));
			return new_vec;
		}

		std::shared_ptr<Eigen::VectorXd> getVector() {
			return _vec;
		}
};
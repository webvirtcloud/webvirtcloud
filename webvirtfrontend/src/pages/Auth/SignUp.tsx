import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import tw from 'twin.macro';

import { signUp } from '@/api/account';
import { Button } from '@/components/Button';
import Input from '@/components/Input';

interface IFormInputs {
  email: string;
  password: string;
}

const SignUp = (): JSX.Element => {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isValid },
  } = useForm<IFormInputs>({ mode: 'onChange' });
  const navigate = useNavigate();

  const onSubmit = async (data: IFormInputs) => {
    try {
      const response = await signUp(data);

      window.localStorage.setItem('token', response.token);

      navigate('/');
    } catch (error) {}
  };

  return (
    <>
      <h1 css={tw`mb-8 text-2xl font-bold text-center`}>Create an account</h1>
      <form
        onSubmit={handleSubmit(onSubmit)}
        css={tw`p-8 space-y-4 rounded-md shadow bg-base`}
      >
        <Input
          id="email"
          label="Email"
          type="email"
          placeholder="account@gmail.com"
          {...register('email', {
            required: 'Email is required.',
            pattern: {
              value: /\S+@\S+\.\S+/,
              message: 'Entered value does not match email format',
            },
          })}
          size="lg"
          required
          error={errors.email?.message}
        />
        <Input
          id="password"
          label="Password"
          type="password"
          placeholder="Secure password"
          {...register('password', {
            minLength: { value: 6, message: 'Password should be at least 6 characters.' },
            required: 'Password is required.',
          })}
          size="lg"
          required
          error={errors.password?.message}
        />
        <Button
          size="lg"
          type="submit"
          fullWidth
          loading={isSubmitting}
          disabled={!isValid}
        >
          Create an account
        </Button>
      </form>
      <p css={tw`mt-4 text-center`}>
        Already have an account?{' '}
        <Link css={tw`text-blue-700 transition-colors hover:text-blue-600`} to="/sign-in">
          Sign In
        </Link>
      </p>
    </>
  );
};

export default SignUp;

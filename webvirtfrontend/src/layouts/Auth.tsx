import { Outlet } from 'react-router-dom';
import tw from 'twin.macro';

const AuthLayout = (): JSX.Element => {
  return (
    <div css={tw`min-h-screen flex flex-col items-center justify-center`}>
      <div css={tw`w-full max-w-lg p-4`}>
        <img
          css={tw`w-16 mb-4 mx-auto`}
          src={new URL('/src/assets/images/logo.svg', import.meta.url).href}
          alt="Logotype"
        />
        <Outlet />
      </div>
    </div>
  );
};

export default AuthLayout;

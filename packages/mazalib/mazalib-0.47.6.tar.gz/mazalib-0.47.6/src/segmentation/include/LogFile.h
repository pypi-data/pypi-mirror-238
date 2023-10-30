#ifndef LOGFILE_H
#define LOGFILE_H
#include <iostream>
#include <fstream>
#include <ctime>
#include <iomanip>
#include <string>

	class LogFile
	{
		public:
			~LogFile();
	    static const LogFile& Instance()
        {
                static LogFile mInstance;
                return mInstance;
        }

		static void SetFileName(const char *FileName)
		{
			instance()->mFileName.assign(FileName);

		}

		static LogFile* instance()
		{
			static LogFile theSingleInstance;
			return &theSingleInstance;
		}
		static void Assert(bool b, const char *msg, const char *FileName)
		{
			if (!b)
			{
				if (FileName == "")
					WriteData(instance()->mFileName.c_str(), msg);
				else
					WriteData(FileName, msg);

				// TODO: Enable for WINDOWS
				//__debugbreak();
			}
		}

		static int WriteData (const char *FileName,const char*s)
		{
			//std::string S(s);
			//WriteData (FileName,S);
			return 0;
		}

		static int WriteData(const char *FileName, const char*s, double v)
		{
			//std::string sv=std::to_string(v);
			//std::string S(s);
			//S.append(sv);
			//WriteData(FileName, S);
			return 0;
		}

		static int WriteData(const char *FileName, const char*s, int v)
		{
			//std::string sv = std::to_string(v);
			//std::string S(s);
			//S.append(sv);
			//WriteData(FileName, S);
			return 0;
		}

		static int WriteData(const char *FileName, const char*s, int64_t v)
		{
			//std::string sv = std::to_string(v);
			//std::string S(s);
			//S.append(sv);
			//WriteData(FileName, S);
			return 0;
		}

		static int WriteData(const char *FileName, const char*s, size_t v)
		{
			//std::string sv = std::to_string(v);
			//std::string S(s);
			//S.append(sv);
			//WriteData(FileName, S);
			return 0;
		}

		static int WriteData(const char *FileName, const char*s, char *c[], double v[], int n)
		{
			//std::string S(s);
			//std::string sv,sc;
			//for (int i = 0; i < n; i++)
			//{
			//	sc.clear();
			//	sc = sc.append(c[i]); sc.append("=");
			//	sv = std::to_string(v[i]);
			//	S.append(sc);
			//	S.append(sv);
			//}
			//WriteData(FileName, S);
			return 0;
		}

	    static int WriteData (const char *FileName,std::string &Data)
        {
   //         std::ofstream O;
			//O.open(FileName,std::ofstream::app);
			//if (!O.is_open())
			//	return -1;
			//std::time_t now = std::time(NULL);
			//std::tm *local_t=localtime(&now);
			//O<<std::put_time(local_t, "%c %Z") <<" "<<Data.c_str() <<std::endl;
			//O.close();    
			return 0;
        }

		static int Clear(const char *FileName)
		{
			//std::ofstream O;
			//O.open(FileName, std::ofstream::out | std::ofstream::trunc);
			//O.close();
			return 0;
		}
		private:
			std::string mFileName;
			LogFile();
			LogFile(std::string &FileName);
	};
#endif
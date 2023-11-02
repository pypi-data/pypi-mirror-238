class Pracklr:
    def avail_prog():
        avail_lx = r"""
        1.  *****Factorial  Using C#.Net Framework*****

	using System;
	using System.Collections.Generic;
	using System.ComponentModel;
	using System.Data;
	using System.Drawing;
	using System.Linq;
	using System.Text;
	using System.Threading.Tasks;
	using System.Windows.Forms;

	namespace Factorial
	{
	    public partial class Form1 : Form
	    {
		
		int a = 1;
		public Form1()
		{
		    InitializeComponent();
		}

		private void button1_Click(object sender, EventArgs e)
		{
		    //For loop Button   
		    int n = Convert.ToInt32(textBox1.Text);
		    for (int i = 1; i <= n; i++)
		    {
		        a = a * i;
		    }
		    textBox2.Text = a.ToString();

		}

		private void button2_Click(object sender, EventArgs e)
		{
		    // While loop button
		    a = 1;
		    textBox2.Text = "";
		    int i = 1, n = Convert.ToInt32(textBox1.Text);
		    while (i <= n)
		    {
		        a = a * i;
		        i++;
		    }
		    textBox2.Text = Convert.ToString(a);
		}

		private void button3_Click(object sender, EventArgs e)
		{
		    // Do While Button
		    int a = 1;
		    textBox2.Text = "";
		    int i = 1, n = Convert.ToInt32(textBox1.Text);
		    do
		    {
		        a = a * i;
		        i++;
		    }
		    while (i <= n);
		    textBox2.Text = Convert.ToString(a);
		}

		private void button4_Click(object sender, EventArgs e)
		{
		    // Close Button
		    this.Close();
		}

		private void button5_Click(object sender, EventArgs e)
		{
		    //Clear Button
		    textBox2.Text = "";
		    textBox1.Text = "";
		}
	    }
	    }


	2.  ***String Operations Using C#.Net Framework****

	using System;
	using System.Collections.Generic;
	using System.ComponentModel;
	using System.Data;
	using System.Drawing;
	using System.Linq;
	using System.Text;
	using System.Threading.Tasks;
	using System.Windows.Forms;

	namespace string_operation
	{
	    public partial class Form1 : Form
	    {
		public Form1()
		{
		    InitializeComponent();
		}

		private void button1_Click(object sender, EventArgs e)
		{
		    //String Length Button
		    String a = textBox1.Text;
		    textBox3.Text = Convert.ToString(a.Length);
		}

		private void button3_Click(object sender, EventArgs e)
		{
		    //String LowerCase Button
		    textBox3.Text = "";
		    String a = textBox1.Text;
		    textBox3.Text = a.ToLower();
		}

		private void button4_Click(object sender, EventArgs e)
		{
		    //String UpperCase Button
		    textBox3.Text = "";
		    String a = textBox1.Text;
		    textBox3.Text = a.ToUpper();
		}

		private void button10_Click(object sender, EventArgs e)
		{
		    //Clear Button
		    textBox1.Text = "";
		    textBox2.Text = "";
		    textBox3.Text = "";
		    textBox4.Text = "";

		}

		private void button9_Click(object sender, EventArgs e)
		{
		    // String Concatenation Button
		    textBox3.Text = "";
		    textBox3.Text = textBox1.Text + textBox2.Text;

		}

		private void button6_Click(object sender, EventArgs e)
		{
		    //String Comparision Button 
		    textBox3.Text = "";
		    textBox3.Text = Convert.ToString(string.Equals(textBox1.Text, textBox2.Text));
		}

		private void button8_Click(object sender, EventArgs e)
		{
		    //String Reverse Button
		    textBox3.Text = "";
		    char[] x = textBox1.Text.ToCharArray();
		    for(int i=x.Length-1;i>=0;i--)
		    {
		        textBox3.Text = textBox3.Text+x[i];
		    }
		}

		private void button7_Click(object sender, EventArgs e)
		{
		    //Strncat Button
		    textBox3.Text = "";
		    String a = textBox1.Text;
		    String y = textBox2.Text;
		    string m = "", k = "";
		    char[] x = a.ToCharArray();
		    char[] c = y.ToCharArray();
		    int n = Convert.ToInt32(textBox4.Text);
		    for(int i=0;i<n;i++)
		    {
		        m = m +x[i];
		    }
		    for (int j = 0; j < n; j++)
		    {
		        k = k +c[j];
		    }
		    textBox3.Text = m+k;
		}

		private void button5_Click(object sender, EventArgs e)
		{
		    //String Duplicate Button
		    string a = textBox1.Text;
		    textBox3.Text = textBox1.Text;

		}

		private void button2_Click(object sender, EventArgs e)
		{
		    //String Copy Button
		    string a = textBox1.Text;
		    textBox3.Text = textBox1.Text;
		}
	    }
	}


	3.  *****Array Operations Using C#.Net Framework*****

	using System;
	using System.Collections.Generic;
	using System.ComponentModel;
	using System.Data;
	using System.Drawing;
	using System.Linq;
	using System.Text;
	using System.Threading.Tasks;
	using System.Windows.Forms;

	namespace WindowsFormsApplication4
	{
	    public partial class Form1 : Form
	    {
		int[] arr = new int[100];
		int a;
		public Form1()
		{
		    InitializeComponent();
		}

		private void Form1_Load(object sender, EventArgs e)
		{

		}

		private void button2_Click(object sender, EventArgs e)
		{
		    //Add Button 
		    if (textBox1.Text == "")
		    {
		        MessageBox.Show("Please Enter SOME VALUES ");
		    }
		    else
		    {
		        listBox1.Items.Add(textBox1.Text);
		        a = listBox1.Items.Count;
		        for (int i = 0; i <= listBox1.Items.Count - 1; i++)
		        {
		            arr[i] = Convert.ToInt32(listBox1.Items[i]);
		        }
		    }

		    
		}

		private void button4_Click(object sender, EventArgs e)
		{
		    //Redim Button
		    int x = Convert.ToInt32(textBox3.Text);
		    for (int j = 1; j <= Convert.ToInt32(textBox2.Text); j++)
		    {
		        arr[x - 1] = 0;
		        x = x + 1;
		    }
		    listBox2.Items.Clear();
		    for (int k = 0; k <= arr.Count() - 1; k++)
		    {
		        if (arr[k] != 0)
		        {
		            listBox2.Items.Add(arr[k].ToString());
		        }
		    }
		}

		private void button1_Click(object sender, EventArgs e)
		{
		    //Reverse Button 
		    Array.Reverse(arr);
		    listBox2.Items.Clear();
		    for (int j = 0; j <= arr.Count() - 1; j++)
		    {
		        if (arr[j] != 0)
		        {
		            listBox2.Items.Add(arr[j].ToString());
		        }
		    }
		}

		private void button3_Click(object sender, EventArgs e)
		{
		    //Sort Button
		    Array.Sort(arr);
		    listBox4.Items.Clear();
		    for (int j = 0; j <= arr.Count() - 1; j++)
		    {
		        if (arr[j] != 0)
		        {
		            listBox4.Items.Add(arr[j].ToString());
		        }
		    }
		}

		private void button5_Click(object sender, EventArgs e)
		{
		    //Clear Button
		    listBox1.Items.Clear();
		    listBox2.Items.Clear();
		    listBox4.Items.Clear();
		    textBox1.Text = "";
		    textBox2.Text = "";
		    textBox3.Text = "";
		}
	    }
	}

	4.  *****Linq  Using C#.Net Framework*****

	using System;
	using System.Collections.Generic;
	using System.ComponentModel;
	using System.Data;
	using System.Drawing;
	using System.Linq;
	using System.Text;
	using System.Threading.Tasks;
	using System.Windows.Forms;

	namespace linq
	{
	    public partial class Form1 : Form
	    {
		string[] v = new string[100];
		int i = 0;
		int length = 0;
		public Form1()
		{
		    InitializeComponent();
		}

		private void button1_Click(object sender, EventArgs e)
		{
		    //Search By Length
		    if (textBox2.Text == "")
		    {
		        MessageBox.Show("Please enter the correct input");
		    }
		    else
		    {
		        length = Convert.ToInt32(textBox2.Text);
		        var res = from s in v where s != null && s.Length == length select s;
		        output.Items.Clear();
		        foreach (string j in res)
		        {
		            if (j != null)
		            {
		                output.Items.Add(j);
		            }
		        }
		    }

		}

		private void button2_Click(object sender, EventArgs e)
		{
		    //Add Button
		    if (textBox1.Text == "")
		    {
		        MessageBox.Show("Please enter some values");
		    }
		    else
		    {
		        if (i < v.Length)
		        {
		            v[i] = textBox1.Text;
		            i = i + 1;
		            input.Items.Add(textBox1.Text);
		        }
		        else
		        {
		            MessageBox.Show("You are allowed to enter upto six values only");
		        }
		    }

		              
		               
		}

		private void button3_Click(object sender, EventArgs e)
		{
		    //Ascending Button
		    var res = from s in v orderby s ascending select s;
		    output.Items.Clear();
		    if (res != null)
		    {
		        foreach (string j in res)
		        {
		            if (j != null)
		            {
		                output.Items.Add(j);
		            }
		        }
		    }
		}

		private void button4_Click(object sender, EventArgs e)
		{
		    //Descending Button
		    var res = from s in v orderby s descending select s;
		    output.Items.Clear();
		    if (res != null)
		    {
		        foreach (string j in res)
		        {
		            if (j != null)
		            {
		                output.Items.Add(j);
		            }
		        }
		    }

		}

		private void button5_Click(object sender, EventArgs e)
		{
		    //Distinct
		    var res = from s in v.Distinct() select s;
		    output.Items.Clear();
		    if (res != null)
		    {

		        foreach (string j in res)
		        {
		            if (j != null)
		            {
		                output.Items.Add(j);
		            }
		        }
		    }
		}

	       

		
	    }
	}

	5.  ***** SortedList Collection Using VB.Net Framework *****

	Public Class Form1
	    Dim i, j, k As Integer
	    Dim a As Integer
	    Dim x, y, z As Object
	    Dim result As Boolean
	    Dim list As New SortedList
	    Private li1, li2 As System.Collections.IList
	    Private Sub Button13_Click(sender As Object, e As EventArgs) Handles Button13.Click
		'Add Button
		Try
		    x = TextBox1.Text
		    y = TextBox2.Text
		    list.Add(x, y)
		    TextBox1.Text = ""
		    TextBox2.Text = ""
		    Button1_Click(sender, e)
		Catch ex As Exception
		    MsgBox("error")
		End Try
	    End Sub


	    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
		'GetValueList Button
		ListBox1.Items.Clear()
		li1 = list.GetValueList()
		i = list.Count
		For j = 0 To i - 1
		    ListBox1.Items.Add(li1(j))
		Next j

	    End Sub

	    Private Sub Button6_Click(sender As Object, e As EventArgs) Handles Button6.Click
		'GetKeylist Button
		ListBox1.Items.Clear()
		li1 = list.GetKeyList()
		i = list.Count
		For j = 0 To i - 1
		    ListBox1.Items.Add(li1(j))
		Next j
	    End Sub

	    Private Sub Button8_Click(sender As Object, e As EventArgs) Handles Button8.Click
		'Clear Button
		list.Clear()
		ListBox1.Items.Clear()
		TextBox1.Text = ""
		TextBox2.Text = ""
	    End Sub

	    Private Sub Button11_Click(sender As Object, e As EventArgs) Handles Button11.Click
		'IndexofKey Button
		z = InputBox("enter the key:")
		TextBox3.Text = list.IndexOfKey(z)

	    End Sub

	    Private Sub Button10_Click(sender As Object, e As EventArgs) Handles Button10.Click
		'GetKey Button
		i = InputBox("enter the index")
		MsgBox("Index key:" + list.GetKey(i))
	    End Sub

	    Private Sub Button9_Click(sender As Object, e As EventArgs) Handles Button9.Click
		'IndexofValue Button
		z = InputBox("enter the value:")
		TextBox3.Text = list.IndexOfValue(z)


	    End Sub

	    Private Sub Button7_Click(sender As Object, e As EventArgs) Handles Button7.Click
		'ContainsValue Key
		z = InputBox("Enter the value to serach:")
		result = list.ContainsValue(z)
		If result = True Then
		    MsgBox("The sorted list contains the value" + z)
		ElseIf result = False Then
		    MsgBox("the sorted list does not contains the value" + z)
		End If
	    End Sub

	    Private Sub Button2_Click(sender As Object, e As EventArgs) Handles Button2.Click
		'Contain Button
		z = InputBox("Enter the key to serach:")
		result = list.ContainsKey(z)
		If result = True Then
		    MsgBox("The sorted list contains the key" + z)
		ElseIf result = False Then
		    MsgBox("the sorted list does not contains the key" + z)
		End If
	    End Sub

	    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.Click
		'GetByIndex Button
		i = InputBox("Enter the index:")
		MsgBox("Index Value:" + list.GetByIndex(i))

	    End Sub

	    Private Sub Button4_Click(sender As Object, e As EventArgs) Handles Button4.Click
		'RemoveAtutton
		i = InputBox("Enter the index to remove")
		list.RemoveAt(i)
		GetValueList_Click(sender, e)
	    End Sub


	    Private Sub Button12_Click(sender As Object, e As EventArgs) Handles Button12.Click
		'Exit Button
		Close()
	    End Sub



	    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click
		'Remove Button
		z = InputBox("ENter the key to remove")
		If list.ContainsKey(z) Then
		    list.Remove(z)
		    MsgBox(z + "is removed")
		Else : MsgBox(z + "is not present in the list")
		End If
		GetValueList_Click(sender, e)

	    End Sub

	    Private Sub GetValueList_Click(sender As Object, e As EventArgs)
		'Throw New NotImplementedException()
	    End Sub
	End Class

	6.  ****Class Library Create And Empsalary****

	****Class Library Code*****
	Public Class calculatesal
	    Dim salary As Double
	    Dim da As Double
	    Dim hra As Double
	    Dim netpay As Double

	    Public Function calc(ByVal sal As Double) As Double
		Dim c1 = New calculatesal()
		Dim k() As Double
		salary = sal
		da = (sal / 10)
		hra = (sal / 20)
		netpay = salary + da + hra
		Return (netpay)
	    End Function
	End Class

	***Visual Program Code employee**
	Imports Empsalary
	Public Class Form1
	    Dim cls As New calculatesal()
	    Dim sal As Integer
	    Dim np As Double
	    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
		calc()
	    End Sub
	    Public Function calc()
		If TextBox1.Text = "" Then
		    MsgBox("Please enter the proper number")
		Else
		    sal = Convert.ToInt32(TextBox1.Text)
		    np = cls.calc(sal)
		    TextBox2.Text = np.ToString()
		End If
	    End Function
	End Class

	7.  ****Sending Email program Using VB.Net Framework*****

	Imports System
	Imports System.Net.Mail
	Public Class Form1
	    Dim fileod As New OpenFileDialog
	    Private Sub Attach_Click(sender As Object, e As EventArgs) Handles Attach.Click
		'Send Button
		Try
		    Dim Smtp_Server As New SmtpClient
		    Dim e_mail As New MailMessage()
		    Dim attachment As System.Net.Mail.Attachment
		    Smtp_Server.UseDefaultCredentials = False
		    Smtp_Server.Credentials = New Net.NetworkCredential("sathish200w@gmail.com", "jatqtmvoebspyrcb")
		    Smtp_Server.Port = 587
		    Smtp_Server.EnableSsl = True
		    Smtp_Server.Host = "smtp.gmail.com"
		    e_mail = New MailMessage()
		    e_mail.From = New MailAddress(TextBox1.Text)
		    e_mail.To.Add(TextBox2.Text)
		    e_mail.Subject = TextBox4.Text
		    e_mail.IsBodyHtml = False
		    e_mail.Body = TextBox3.Text
		    attachment = New System.Net.Mail.Attachment(TextBox5.Text) 'file path e_mail.Attachments.Add(attachment)
		    Smtp_Server.Send(e_mail)
		    MsgBox("Mail Sent")
		Catch error_t As Exception
		    MsgBox(error_t.ToString)
		End Try
	    End Sub

	    Private Sub Button1_Click(sender As Object, e As EventArgs) Handles Button1.Click
		'Attach Button
		If fileod.ShowDialog Then
		    TextBox5.Text = fileod.FileName.ToString()
		End If
	    End Sub

	End Class



	8.  ****Student Database Manipulation Using VB.Net Framework****

	Imports System.Data.SqlClient
	Public Class Form1
	    Dim con As New SqlConnection
	    Dim cmd As New SqlCommand
	    Dim da As New SqlDataAdapter
	    Dim dt As New DataTable
	    Dim m1, m2, m3, tot As Integer
	    Dim s, z As String
	    Private Sub clicktoupdate_Click(sender As Object, e As EventArgs) Handles Button6.Click
		'ClicktoUpdate Button
		con = New SqlConnection(constr)
		con.Open()
		m1 = CInt(TextBox3.Text)
		m2 = CInt(TextBox4.Text)
		m3 = CInt(TextBox5.Text)
		tot = m1 + m2 + m3
		TextBox6.Text = tot.ToString()
		cmd = New SqlCommand("update stu set name='" + TextBox2.Text + "',Mark1=" & m1 & ", Mark2= " & m2 & ", Mark3 = " & m3 & ", Total= " & tot & " where regno='" + TextBox1.Text + "'", con)
		cmd.ExecuteNonQuery()
		MsgBox("1 Row affected successfully")
		con.Close()
		binding()
	    End Sub
	    Private Sub delete_Click(sender As Object, e As EventArgs) Handles Button3.Click
		'Delete Button 
		con = New SqlConnection(constr)
		z = InputBox("enter the register number to delete")
		Button5.Visible = True
		con.Open()
		cmd = New SqlCommand("select * from stu where regno='" + z + "'", con)
		da = New SqlDataAdapter(cmd)
		dt.Clear()
		da.Fill(dt)
		If (dt.Rows.Count = vbEmpty) Then
		    MsgBox("There is no value matched with your search")
		Else
		    If (dt.Rows.Count = vbEmpty) Then
		        MsgBox("There is no value matched with your search")
		    Else
		        cmd = New SqlCommand("delete from stu where regno='" + z + "'", con)
		        cmd.ExecuteNonQuery()
		        MsgBox("1 row affected")
		    End If
		    binding()
		End If
	    End Sub
	    Private Sub Form1_Load(sender As Object, e As EventArgs) Handles MyBase.Load
		'TODO: This line of code loads data into the 'Student_DetailsDataSet.Student_Details' table. You can move, or remove it, as needed.
		Me.Student_DetailsTableAdapter.Fill(Me.Student_DetailsDataSet.Student_Details)
		'TODO: This line of code loads data into the 'StudentsDataSet.stu' table. You can move, or remove it, as needed.
		'Me.StuTableAdapter.Fill(Me.StudentsDataSet.stu)
		'TODO: This line of code loads data into the 'Student1DataSet.Table' table. You can move, or remove it, as needed.
		binding()
	    End Sub
	    Private Sub navigate_Click(sender As Object, e As EventArgs) 
		Me.Hide()
		Form2.Show()
	    End Sub

	    Private Sub Button3_Click(sender As Object, e As EventArgs) Handles Button3.Click

	    End Sub

	    Private Sub Button5_Click(sender As Object, e As EventArgs) Handles Button5.Click
		'Close Button
		Close()
	    End Sub

	    Dim constr As String = "Data Source=DESKTOP-K971CDE\SQLEXPRESS;Initial Catalog=students;Integrated Security=True;Pooling=False"
	    Private Sub update_Click(sender As Object, e As EventArgs) Handles Button2.Click
		'Update Button
		con = New SqlConnection(constr)
		s = InputBox("enter the register number to update")
		TextBox1.Text = s
		TextBox1.Enabled = False
		Button3.Visible = True
		con.Open()
		cmd = New SqlCommand("select * from stu where regno='" + TextBox1.Text + "'", con)
		da = New SqlDataAdapter(cmd)
		dt.Clear()
		da.Fill(dt)
		If (dt.Rows.Count = vbEmpty) Then
		    MsgBox("There is no value matched with your search")
		Else
		    TextBox2.Text = dt.Rows(0).Item(1)
		    TextBox3.Text = dt.Rows(0).Item(2)
		    TextBox4.Text = dt.Rows(0).Item(3)
		    TextBox5.Text = dt.Rows(0).Item(4)
		    TextBox6.Text = dt.Rows(0).Item(5)
		    con.Close()
		End If
		binding()
	    End Sub
	    Private Sub insert_Click(sender As Object, e As EventArgs) Handles Button1.Click
		'Insert
		con = New SqlConnection(constr)
		If (TextBox1.Text = "" Or TextBox2.Text = "" Or TextBox3.Text = "" Or TextBox4.Text = "" Or TextBox5.Text = "") Then
		    MsgBox("Please enter the missing columns")
		Else
		    con.Open()
		    m1 = CInt(TextBox3.Text)
		    m2 = CInt(TextBox4.Text)
		    m3 = CInt(TextBox5.Text)
		    tot = m1 + m2 + m3
		    TextBox6.Text = tot.ToString()
		    cmd = New SqlCommand("insert into stu values('" + TextBox1.Text + "','" + TextBox2.Text + "'," & m1 & "," & m2 & "," & m3 & "," & tot & ")", con)
		    cmd.ExecuteNonQuery()
		    MsgBox("1 Row inserted successfully")
		    con.Close()
		    binding()
		End If
	    End Sub
	    Public Sub binding()
		con = New SqlConnection(constr)
		con.Open()
		cmd = New SqlCommand("select * from stu", con)
		da = New SqlDataAdapter(cmd)
		dt.Clear()
		da.Fill(dt)
		DataGridView1.DataSource = dt
	    End Sub
	End Class
		
        
        """
        return avail_lx
    
